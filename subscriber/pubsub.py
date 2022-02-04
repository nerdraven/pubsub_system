# pylint: disable=missing-function-docstring,missing-module-docstring,missing-class-docstring,invalid-name

from dataclasses import dataclass

@dataclass(frozen=True)
class Message:
    attributes: dict
    data: str
    messageId: str
    message_id: str
    publishTime: str
    publish_time: str

    @classmethod
    def from_dict(cls, data: dict):
        return Message(**data)

@dataclass(frozen=True)
class PushMessage:
    subscription: str
    message: Message

    @classmethod
    def from_dict(cls, data: dict):
        return PushMessage(
            data["subscription"],
            Message.from_dict(data["message"])
        )
