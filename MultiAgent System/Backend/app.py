from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
  dictionary = {"name": "Santiago", "lastName": "Alducin"}
  print(dictionary)
  return dictionary