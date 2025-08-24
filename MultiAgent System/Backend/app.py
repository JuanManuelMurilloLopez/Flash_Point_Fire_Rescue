from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
  dictionary = {"name": "Santiago", "last_name": "Alducin"}
  return dictionary