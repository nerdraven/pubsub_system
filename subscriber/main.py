# pylint: disable=missing-function-docstring,missing-class-docstring,missing-module-docstring

import os
import base64

from flask import Flask, request
from google.protobuf.message import DecodeError

import protocol.event_pb2 as pb
from subscriber.pubsub import PushMessage

app = Flask(__name__)

@app.route("/", methods=["POST"])
def index():
    envelope = request.get_json()
    print(envelope)

    try:
        data = PushMessage.from_dict(envelope)
    except KeyError:
        msg = "Invalid request"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    attributes = data.message.attributes
    event_type = attributes["type"]

    data = base64.b64decode(data.message.data)

    event = pb.Event()
    try:
        event.ParseFromString(data)
    except (DecodeError, RuntimeWarning):
        print("Protobuf was invalid")

    print("Event type")
    print(event_type)

    print("Recieved event")
    print(event)

    return ("", 204)


if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    app.run(host="127.0.0.1", port=PORT, debug=True)
