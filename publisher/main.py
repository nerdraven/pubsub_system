# pylint: disable=missing-function-docstring,missing-module-docstring
import os
from flask import Flask, request
from publisher.pubsub import publish_to_pubsub

app = Flask(__name__)

@app.route("/")
def index():
    return "", 204

@app.route("/publish")
def publish_message():

    message = "Hello World"
    if data := request.args.get("message", ""):
        message = data

    msg_id = publish_to_pubsub(message)
    if msg_id := publish_to_pubsub(message):
        return f"Published message. Id: {msg_id}", 200
    return "An error occured in publishing"

if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    app.run(host="127.0.0.1", port=PORT, debug=True)
