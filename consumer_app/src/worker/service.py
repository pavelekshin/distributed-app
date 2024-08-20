import secrets
from datetime import datetime
from typing import Any

from src.database import fetch_one, message
from src.model import UserData


async def insert_message(url: str, data: UserData) -> dict[str, Any] | None:
    insert_query = (
        message.insert()
        .values(
            {
                "message_id": data.msg_id,
                "data": data.model_dump_json(),
                "code": secrets.token_urlsafe(8),
                "original_url": url,
                "created_at": datetime.now(),
            }
        )
        .returning(message)
    )
    return await fetch_one(insert_query)
