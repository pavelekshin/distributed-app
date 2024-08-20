from datetime import datetime
from typing import Any

from src.database import fetch_one, message, subscribe
from src.model import Message


async def get_row_by_code(code: str) -> dict[str, Any] | None:
    """
    Check code in table
    :param code: code
    :return: dict or None
    """
    select_query = message.select().where(message.c.code == code)
    return await fetch_one(select_query)


async def insert_message(
    code: str, data: Message, status: bool
) -> dict[str, Any] | None:
    """
    Insert data in table
    :param code: code
    :param data: Message
    :param status: bool
    :return: dict or None
    """
    insert_query = (
        subscribe.insert()
        .values(
            {
                "code": code,
                "is_unsubscribe": status,
                "acc_id": data.data.acc_id,
                "created_at": datetime.now(),
            }
        )
        .returning(subscribe)
    )
    return await fetch_one(insert_query)
