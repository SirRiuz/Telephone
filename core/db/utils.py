# Python
from typing import Optional
import sys

# Libs
from core.db.exceptions.database import DataBaseConfigException, InvalidEngine
from core.db.exceptions.database import InvalidEngine
from core.db.constants import (
    ALLOWED_ENGINES,
    POSTGRESQL_ENGINES,
    TEST_DATABASE_NAME,
    SQLITE_ENGINES,
)

try:
    from core.settings import DATABASE
except ImportError:
    DATABASE = {}


def validate_database_config(config: dict):
    """
    Validates that the required parameters for
    connection configuration are present.
    """
    required_keys = ["ENGINE", "NAME"]
    if config["ENGINE"] in POSTGRESQL_ENGINES:
        required_keys += ["USER", "PASSWORD", "HOST", "PORT"]

    for key in required_keys:
        if key not in config or not config[key]:
            raise DataBaseConfigException(
                f"The '{key}' value is required for the database configuration.",
            )


def build_db_uri(
    engine: str = SQLITE_ENGINES,
    user: str = None,
    password: str = None,
    host: str = None,
    port: str = None,
    name: str = None,
) -> str:
    """Builds the database connection URL."""

    if engine == POSTGRESQL_ENGINES:
        return f"postgresql://{user}:{password}" f"@{host}:{port}/{name}"

    return f"sqlite:///./{name}"


def get_db_uri() -> Optional[str]:
    """Retrieves the database connection URL."""

    # Creates a database during testing.
    if "pytest" in sys.modules:
        return build_db_uri(name=TEST_DATABASE_NAME)

    if not DATABASE:
        return ""

    engine = DATABASE.get("ENGINE")
    if engine not in ALLOWED_ENGINES:
        raise InvalidEngine(f"The database engine '{engine}' is not supported.")

    validate_database_config(DATABASE)

    if engine in POSTGRESQL_ENGINES:
        return build_db_uri(
            engine=POSTGRESQL_ENGINES,
            user=DATABASE["USER"],
            password=DATABASE["PASSWORD"],
            host=DATABASE["HOST"],
            port=DATABASE["PORT"],
            name=DATABASE["NAME"],
        )

    return build_db_uri(name=DATABASE["NAME"])
