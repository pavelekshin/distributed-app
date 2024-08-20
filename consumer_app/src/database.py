from typing import Any

from sqlalchemy import (
    Column,
    CursorResult,
    DateTime,
    Identity,
    Insert,
    Integer,
    MetaData,
    Select,
    String,
    Table,
    Text,
    Update,
    func,
)
from sqlalchemy.ext.asyncio import async_engine_from_config

from src.settings import db_settings, settings

DB_NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_`%(constraint_name)s`",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

DATABASE_URL = str(settings.DATABASE_URL)

engine = async_engine_from_config(db_settings.config)
metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

message: Table = Table(
    "message",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("message_id", String(40), nullable=False),
    Column("code", String(8), nullable=False, index=True, unique=True),
    Column("data", Text, nullable=False),
    Column("original_url", String(256), nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
)


async def fetch_one(select_query: Select | Insert | Update) -> dict[str, Any] | None:
    async with engine.begin() as conn:
        cursor: CursorResult = await conn.execute(select_query)
        result = cursor.first()
        return result._asdict() if result else None
