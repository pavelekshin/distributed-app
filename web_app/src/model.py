import json
from datetime import datetime
from typing import Any

from pydantic import BaseModel, field_validator


class UserData(BaseModel):
    acc_id: str
    unsubscribe: bool
    msg_id: str


class Message(BaseModel):
    id: int
    message_id: str
    code: str
    data: UserData
    original_url: str
    created_at: datetime

    @field_validator("data", mode="before")
    @classmethod
    def parse_data(cls, value: str | dict) -> dict[str, Any]:
        if isinstance(value, str):
            return json.loads(value)
        return value
