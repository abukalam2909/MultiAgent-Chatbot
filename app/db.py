from __future__ import annotations

from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from app.config import get_settings


def _build_mysql_url() -> str:
    settings = get_settings()
    user = quote_plus(settings.mysql_user)
    password = quote_plus(settings.mysql_password)
    host = settings.mysql_host
    port = settings.mysql_port
    db = settings.mysql_db
    return f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}"


def get_engine() -> Engine:
    return create_engine(_build_mysql_url())


def run_query(sql: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text(sql), params or {})
        rows = result.fetchall()
        cols = result.keys()
    return [dict(zip(cols, row)) for row in rows]
