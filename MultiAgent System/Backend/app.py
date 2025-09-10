import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from flask import Flask
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

plt.rcParams["animation.html"] = "jshtml"
matplotlib.rcParams["animation.embed_limit"] = 2**128

import numpy as np
import pandas as pd
import seaborn as sns

sns.set()

import time
import datetime

from Models.Fire import Fire
from Models.Firefighter import Firefighter
from Models.FireRescueModel import FireRescueModel


app = Flask(__name__)

model = FireRescueModel(strategy="intelligent")

ITERATIONS = 100
i = 0

while not (model.defeat()) and not (model.victory()) and i < ITERATIONS:
    model.step()
    i += 1

allAgentsInfo = model.datacollector.get_agent_vars_dataframe()
allGrids = model.datacollector.get_model_vars_dataframe()

agents_by_step = {}
for (step, agent_id), row in allAgentsInfo.iterrows():
    d = row.to_dict()
    d["AgentID"] = agent_id
    d["Action"] = row["Action"]
    agents_by_step.setdefault(step, []).append(d)

grids_by_step = {}
for step, row in allGrids.iterrows():
    grids_by_step[step] = row.to_dict()


@app.route("/step/<int:stepNumber>")
def step(stepNumber):
    agents = agents_by_step.get(stepNumber)
    grid = grids_by_step.get(stepNumber)
    if agents is None or grid is None:
        from flask import abort

        abort(404, description=f"Step {stepNumber} not found")
    # Parse fires
    fires_raw = grid.get("NewFire", [])
    if isinstance(fires_raw, str):
        import ast

        fires_raw = ast.literal_eval(fires_raw)
    fires = [
        {
            "state": f.get("state", ""),
            "position": {
                "x": f.get("position", (None, None))[0],
                "z": f.get("position", (None, None))[1],
            },
        }
        for f in fires_raw
    ]
    # Parse dices
    dices = grid.get("Dices", {"red": 0, "black": 0})
    if isinstance(dices, str):
        import ast

        dices = ast.literal_eval(dices)
    # Parse damage
    damage = grid.get("DamageTokens", 0)
    # Parse POIs
    pois_raw = grid.get("ChangedPOIs", [])
    if isinstance(pois_raw, str):
        import ast

        pois_raw = ast.literal_eval(pois_raw)
    poi = []
    for p in pois_raw:
        pos = p.get("position", (None, None))
        if p.get("Victim", 0) == 0:
            state = "fake"
        elif p.get("Victim", 0) == 1 and not p.get("Rescued", False):
            state = "alive"
        elif p.get("Victim", 0) == 1 and p.get("Rescued", False):
            state = "rescued"
        else:
            state = "dead"
        poi.append({"state": state, "position": {"x": pos[0], "z": pos[1]}})
    # Build players list with id and position only
    players = []
    for agent_data in agents:
        pos = agent_data.get("Position", (None, None))
        player = {
            "id": agent_data.get("AgentID"),  # You may need to pass AgentID explicitly
            "position": {"x": pos[0], "z": pos[1]},
            # No actions or state available currently
        }
        players.append(player)
    response = {
        "players": players,
        "fires": fires,
        "dices": dices,
        "poi": poi,
        "damage": damage,
    }
    print("Sending response:")
    return response
