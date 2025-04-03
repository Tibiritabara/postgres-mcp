from psycopg import Connection
from pydantic import BaseModel


class AppContext(BaseModel):
    db_connection: Connection

    class Config:
        arbitrary_types_allowed = True


class TableSummary(BaseModel):
    schema_name: str
    table_name: str
    table_description: str | None


class DatabaseSummary(BaseModel):
    tables: list[TableSummary]


class Column(BaseModel):
    column_name: str
    data_type: str
    is_nullable: bool
    column_default: str | None
    character_maximum_length: int | None
    numeric_precision: int | None
    numeric_scale: int | None


class Table(BaseModel):
    schema_name: str
    table_name: str
    columns: list[Column]
