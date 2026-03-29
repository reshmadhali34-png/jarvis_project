from flask import Flask, request, jsonify, render_template
from jarvis_api import process_command

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/command", methods=["POST"])
def command():
    data = request.json["command"]
    reply = process_command(data)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)