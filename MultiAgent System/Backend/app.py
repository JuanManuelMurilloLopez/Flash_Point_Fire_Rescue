from flask import Flask

app = Flask(__name__)

dict = {
    1: {
        "players": [
            {
                "id": 0,
                "actions": [{"action": "move", "data": {"x": 0, "z": 0}}],
                "state": "alive",
            },
            {
                "id": 1,
                "actions": [{"action": "move", "data": {"x": 5, "z": 5}}],
                "state": "alive",
            },
            {
                "id": 2,
                "actions": [{"action": "move", "data": {"x": 3, "z": 3}}],
                "state": "alive",
            },
        ],
        "fires": [
            {"state": "smoke", "position": {"x": 10, "z": 10}},
            {"state": "fire", "position": {"x": 14, "z": 10}},
            {"state": "explosion", "position": {"x": 14, "z": 10}},
        ],
        "dices": {"red": 3, "black": 5},
        "poi": [
            {"state": "fake", "position": {"x": 10, "z": 10}},
            {"state": "alive", "position": {"x": 10, "z": 10}},
            {"state": "dead", "position": {"x": 10, "z": 10}},
        ],
        "damage": 5,
    },
    2: {
        "players": [
            {
                "id": 1,
                "actions": [{"action": "move", "data": {"x": 10, "z": 10}}],
                "state": "alive",
            },
            {
                "id": 2,
                "actions": [{"action": "move", "data": {"x": 10, "z": 10}}],
                "state": "alive",
            },
            {
                "id": 3,
                "actions": [{"action": "move", "data": {"x": 10, "z": 10}}],
                "state": "alive",
            },
        ]
    },
    3: {
        "players": [
            {
                "id": 1,
                "actions": [{"action": "move", "data": {"x": 10, "z": 10}}],
                "state": "alive",
            },
            {
                "id": 2,
                "actions": [{"action": "move", "data": {"x": 10, "z": 10}}],
                "state": "alive",
            },
            {
                "id": 3,
                "actions": [{"action": "move", "data": {"x": 10, "z": 10}}],
                "state": "alive",
            },
        ]
    },
    4: {
        "players": [
            {
                "id": 1,
                "actions": [{"action": "move", "data": {"x": 10, "z": 10}}],
                "state": "alive",
            },
            {
                "id": 2,
                "actions": [{"action": "move", "data": {"x": 10, "z": 10}}],
                "state": "alive",
            },
            {
                "id": 3,
                "actions": [{"action": "move", "data": {"x": 10, "z": 10}}],
                "state": "alive",
            },
        ]
    },
}


@app.route("/step/<int:stepNumber>")
def step(stepNumber):
    return dict[stepNumber]
