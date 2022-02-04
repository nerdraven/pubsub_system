# pylint: disable=missing-function-docstring,missing-module-docstring

import os
import datetime

from google.api_core.exceptions import NotFound
from google.cloud.pubsub import PublisherClient
import protocol.event_pb2 as pb

project_id = os.environ.get("PROJECT_ID")
topic_id = os.environ.get("TOPIC_ID")



def publish_to_pubsub(message: str):
    publisher_client = PublisherClient()
    topic_path = publisher_client.topic_path(project_id, topic_id)  # pylint: disable=no-member

    try:
        # Instantiate a protoc-generated class defined in `event.proto`.
        event = pb.Event()
        event.id = str(int(datetime.datetime.now().timestamp()))
        event.name = message

        attributes = {
            "type": "Event"
        }

        # Encode the data according to the message serialization type.
        data = event.SerializeToString()
        print(f"Preparing a binary-encoded message:\n{data}")

        future = publisher_client.publish(topic_path, data, **attributes)
        msg_id = future.result()
        print(f"Published message ID: {msg_id}")
        return msg_id

    except NotFound:
        print(f"{topic_id} not found.")
