from flask import Flask

app = Flask(__name__)

dict = {
  1: {
    "players": [
      {"id": 1, "x": 10, "y": 10},
      {"id": 2, "x": 10, "y": 10},
      {"id": 3, "x": 10, "y": 10},
    ]
  },
  2: {
    "players": [
      {"id": 1, "x": 10, "y": 10},
      {"id": 2, "x": 10, "y": 10},
      {"id": 3, "x": 10, "y": 10},
    ]
  },
  3: {
    "players": [
      {"id": 1, "x": 10, "y": 10},
      {"id": 2, "x": 10, "y": 10},
      {"id": 3, "x": 10, "y": 10},
    ]
  },
  4: {
    "players": [
      {"id": 1, "x": 10, "y": 10},
      {"id": 2, "x": 10, "y": 10},
      {"id": 3, "x": 10, "y": 10},
    ]
  },
}

@app.route("/step/<int:stepNumber>")
def step(stepNumber):
  return dict[stepNumber]