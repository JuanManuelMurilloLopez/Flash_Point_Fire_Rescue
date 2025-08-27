from flask import Flask

app = Flask(__name__)

dict = {
    1: {
        "players": [
            {
                "id": 1,
                "actions": [{"action": "move", "data": {"x": 10, "z": 10}}],
                "state": "alive",
            },
            {
                "id": 1,
                "actions": [{"action": "move", "data": {"x": 10, "z": 10}}],
                "state": "alive",
            },
            {
                "id": 1,
                "actions": [{"action": "move", "data": {"x": 10, "z": 10}}],
                "state": "alive",
            },
        ],
        "fires": [
            {"state": "smoke", "position": {"x": 10, "z": 10}},
            {"state": "fire", "position": {"x": 14, "z": 10}},
            {"state": "explosion", "position": {"x": 14, "z": 10}},
        ],
        "dice": {"red": 1, "black": 5},
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
                "id": 1,
                "actions": [{"action": "move", "data": {"x": 10, "z": 10}}],
                "state": "alive",
            },
            {
                "id": 1,
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
                "id": 1,
                "actions": [{"action": "move", "data": {"x": 10, "z": 10}}],
                "state": "alive",
            },
            {
                "id": 1,
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
                "id": 1,
                "actions": [{"action": "move", "data": {"x": 10, "z": 10}}],
                "state": "alive",
            },
            {
                "id": 1,
                "actions": [{"action": "move", "data": {"x": 10, "z": 10}}],
                "state": "alive",
            },
        ]
    },
}


@app.route("/step/<int:stepNumber>")
def step(stepNumber):
    return dict[stepNumber]
