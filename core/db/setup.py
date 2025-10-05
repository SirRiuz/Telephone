# Python
from typing import Optional

# Libs
from core.db.connection import get_engine
from sqlalchemy.engine import Engine


def setUp() -> Optional[Engine]:
    """It is responsible for initializing the database."""
    from core.db.models import Model

    engine = get_engine()

    if engine:
        Model.metadata.create_all(bind=engine)
        return engine
