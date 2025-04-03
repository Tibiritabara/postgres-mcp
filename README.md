# MCP PostgreSQL Demo

A FastMCP server that enables LLMs to connect and interact with PostgreSQL databases. This project demonstrates how to use the Model Context Protocol (MCP) to allow Language Models to query and explore database schemas and tables.

## Features

- **Schema Exploration**: Retrieve metadata about database schemas
- **Table Inspection**: Get detailed information about table structures
- **Database Querying**: Execute SQL queries against the database
- **YAML Formatting**: Results are returned in YAML format for easy consumption by LLMs

## Resources

The server exposes the following MCP resources:

- `database://{schema}` - Get information about all tables in a schema
- `database://{schema}/tables/{table}` - Get detailed information about a specific table

## Tools

- `query_database` - Execute SQL queries against the database (SELECT queries only)

## Prompts

The server includes the following predefined prompts:

- `prompt_schema_description` - Ask for a description of a database schema
- `prompt_table_description` - Ask for a description of a specific table
- `prompt_query_database` - Ask for data from a specific table

## Prerequisites

- Python 3.12 or higher
- PostgreSQL database
- UV package manager (recommended)

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd mcp-demo
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install UV (if not already installed):

   ```bash
   pip install uv
   ```

4. Install dependencies with UV:

   ```bash
   uv sync
   ```

5. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Update the values according to your PostgreSQL configuration

## Configuration

The application is configured using environment variables:

| Variable    | Description              | Default   |
| ----------- | ------------------------ | --------- |
| APP_NAME    | Application name         | mcp-demo  |
| DB_HOST     | PostgreSQL host          | localhost |
| DB_PORT     | PostgreSQL port          | 5432      |
| DB_USER     | PostgreSQL username      | postgres  |
| DB_PASSWORD | PostgreSQL password      | postgres  |
| DB_NAME     | PostgreSQL database name | postgres  |

## Usage

1. First, uncomment the run function in `src/main.py` by removing the comment from these lines at the bottom of the file:

   ```python
   # if __name__ == "__main__":
   #     print("Starting FastMCP server...")
   #     mcp.run()
   ```

2. Start the FastMCP server:

   ```bash
   python -m src.main
   ```

3. The server will be available for LLMs to connect to and query your PostgreSQL database. With the server running, the MCP can be loaded into client applications for interaction.

### Client Configuration

To use this MCP in a client application, add the following configuration to your client's MCP configuration file (e.g., `.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "postgres-mcp-server": {
      "command": "/path/to/your/venv/bin/mcp",
      "args": ["run", "/path/to/your/postgres-mcp/src/main.py"],
      "env": {
        "APP_NAME": "mcp-demo",
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "DB_USER": "postgres",
        "DB_PASSWORD": "postgres",
        "DB_NAME": "postgres"
      }
    }
  }
}
```

Be sure to replace the paths with the actual paths to your virtual environment and project directory, and update the environment variables to match your PostgreSQL configuration.

## Development

Install development dependencies with UV:

```bash
uv pip install -e ".[dev]"
```

Development tools included:

- JupyterLab for notebooks
- Pyright for type checking
- Ruff for linting

## Docker

To run the application with Docker:

1. Build the Docker image:

   ```bash
   docker build -t mcp-demo .
   ```

2. Run the container:
   ```bash
   docker run --env-file .env.docker -p 8000:8000 mcp-demo
   ```

## Example Usage

### Get Schema Information

```python
from mcp.client import get_client

client = get_client("http://localhost:8000")
schema_info = client.get_resource("database://public")
print(schema_info)
```

### Get Table Details

```python
table_info = client.get_resource("database://public/tables/users")
print(table_info)
```

### Execute a Query

```python
result = client.invoke_tool("query_database", {"query": "SELECT * FROM users LIMIT 10"})
print(result)
```

## License

[Add your license information here]

## Contributors

- Ricardo Santos <ricardo.santos.diaz@gmail.com>
