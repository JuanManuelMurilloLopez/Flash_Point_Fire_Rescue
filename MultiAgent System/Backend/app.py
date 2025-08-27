from flask import Flask

app = Flask(__name__)

dict = {
    1: {
        "players": [
            {
                "id": 0,
                "actions": [{"action": "move", "data": {"x": 10, "z": 10}}],
                "state": "alive",
            },
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
        ]
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
