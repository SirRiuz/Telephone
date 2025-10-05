# Python
from typing import Optional

# Libs
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from core.db.utils import get_db_uri


def get_engine() -> Optional[Engine]:
    """Establishes the database connection."""
    db_uri = get_db_uri()

    if not db_uri:
        return

    engine = create_engine(db_uri)
    return engine
