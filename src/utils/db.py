"""
This module contains the functions to get a database connection.
"""

from collections.abc import Callable
from typing import Any

import psycopg
from psycopg import Connection
from psycopg.rows import tuple_row

from utils.config import get_config


def get_db_connection(row_factory: Callable[[Any], Any] = tuple_row) -> Connection:
    """
    Get a database connection

    Args:
        row_factory: The row factory to use.

    Returns:
        A database connection.
    """
    config = get_config()
    return psycopg.connect(
        host=config.db_host,
        port=config.db_port,
        user=config.db_user,
        password=config.db_password.get_secret_value(),  # pylint: disable=E1101
        dbname=config.db_name,
        row_factory=row_factory,
    )
