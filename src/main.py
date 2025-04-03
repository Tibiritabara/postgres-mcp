"""
This module contains the main entry point for the FastMCP server.
"""

import uuid
from typing import Any

import yaml
from mcp.server.fastmcp import FastMCP
from psycopg.rows import dict_row

from utils.config import get_config
from utils.db import get_db_connection
from utils.types import Column, DatabaseSummary, Table, TableSummary

config = get_config()


mcp = FastMCP(config.app_name)


# Database description resource
@mcp.resource("database://{schema}")
async def get_schema_description(schema: str) -> str:
    """
    Tool to retrieve the description of a database

    Args:
        schema: The name of the postgres schema

    Returns:
        The description of the schema in YAML format
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            query = """
                SELECT
                    n.nspname AS schema_name,
                    c.relname AS table_name,
                    d.description AS table_description
                FROM pg_catalog.pg_class c
                LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
                LEFT JOIN pg_catalog.pg_description d ON d.objoid = c.oid AND d.objsubid = 0
                WHERE
                    c.relkind = 'r'
                    AND n.nspname = %(schema)s
                ORDER BY schema_name, table_name;
            """
            cursor.execute(query, {"schema": schema})
            tables = cursor.fetchall()
    # Map the tables into a DatabaseSummary
    db_summary = DatabaseSummary(
        tables=[
            TableSummary(
                schema_name=table[0],
                table_name=table[1],
                table_description=table[2],
            )
            for table in tables
        ]
    )
    # Serialize the database summary into a YAML string
    yaml_summary = yaml.dump(db_summary.model_dump())
    return yaml_summary


# Add a dynamic table description resource
@mcp.resource("database://{schema}/tables/{table}")
async def get_table_description(schema: str, table: str) -> str:
    """
    Tool to retrieve the description of a table

    Args:
        schema: The name of the postgres schema
        table: The name of the table

    Returns:
        The description of the table in YAML format
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            query = """
                SELECT
                    column_name,
                    data_type,
                    is_nullable,
                    column_default,
                    character_maximum_length,
                    numeric_precision,
                    numeric_scale
                FROM
                    information_schema.columns
                WHERE
                    table_schema = %(schema)s AND
                    table_name = %(table)s
                ORDER BY
                    ordinal_position;
            """
            cursor.execute(query, {"schema": schema, "table": table})
            columns = cursor.fetchall()
    # Map the tables into a DatabaseSummary
    table_obj = Table(
        schema_name=schema,
        table_name=table,
        columns=[
            Column(
                column_name=column[0],
                data_type=column[1],
                is_nullable=column[2],
                column_default=column[3],
                character_maximum_length=column[4],
                numeric_precision=column[5],
                numeric_scale=column[6],
            )
            for column in columns
        ],
    )
    # Serialize the table object into a YAML string
    yaml_summary = yaml.dump(table_obj.model_dump())
    return yaml_summary


@mcp.tool()
async def query_database(query: str) -> str:
    """
    Tool to query the database

    Args:
        query: The query to execute. The query should be a valid SQL query.
            The query must be only a SELECT query.

    Returns:
        The result of the query in YAML format
    """
    with get_db_connection(row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)  # type: ignore
            rows: list[dict[str, Any]] = cursor.fetchall()  # type: ignore
    processed_rows = []
    for row in rows:
        processed_row = {}
        for key, value in row.items():
            # Convert UUID objects to strings
            if isinstance(value, uuid.UUID):
                processed_row[key] = str(value)
            else:
                processed_row[key] = value
        processed_rows.append(processed_row)

    yaml_summary = yaml.dump(processed_rows)
    return yaml_summary


@mcp.prompt()
def prompt_table_description(schema: str, table: str) -> str:
    """
    Tool to retrieve the description of a table

    Args:
        schema: The name of the postgres schema
        table: The name of the table
    """
    return (
        f"Please provide a description of the table `{table}` in the schema `{schema}`"
    )


@mcp.prompt()
def prompt_schema_description(schema: str) -> str:
    """
    Tool to retrieve the description of a schema

    Args:
        schema: The name of the postgres schema
    """
    return f"Please provide a description of the schema `{schema}`"


@mcp.prompt()
def prompt_query_database(schema: str, table: str) -> str:
    """
    Tool to query the database

    Args:
        schema: The name of the postgres schema
        table: The name of the table
    """
    return f"Please bring me the data from the table `{table}` in the schema `{schema}`"
