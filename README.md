# mcp-mysql-server

A simple Python script for interacting with a local MySQL database via standard input/output (stdio), based on FastMCP.

## Overview

`mcp-mysql-server` provides a command-line interface for querying and inspecting the schema of a local MySQL database. It is designed for ease of use in local development environments where a lightweight, script-based interaction is preferred. The script utilizes standard input and output for commands and results, making it easy to integrate with other command-line tools and workflows.

## Features

* **Query Execution:** Execute SQL SELECT statements and view the results in a simple, readable format.
* **Data Manipulation:** Insert data into tables with the write_table tool.
* **Schema Inspection:** Retrieve information about the database schema, including:
    * Listing all tables with the list_tables tool.
    * Displaying the columns and their data types for a specific table with get_table_schema.
* **Connection Testing:** Test database connectivity and get server information.
* **Configurable Access Controls:** Define connection parameters (host, user, password, database) through configuration, allowing secure access to the database.
* **stdio Interface:** Interact with the script using standard input for commands and receive output via standard output, facilitating scripting and automation.
* **Local Deployment Focus:** Optimized for use within local development environments.

## Getting Started

### Prerequisites

* Python 3.x installed on your system.
* A local MySQL server instance running.
* Required Python libraries (install using the requirements.txt file):
    ```bash
    pip install -r requirements.txt
    ```

### Installation

1.  Download or clone the repository to your local machine.

### Configuration

1.  Create a configuration file (e.g., `config.ini`) in the same directory as the script or specify the path when running the script. The configuration file should have the following format:

    ```ini
    [mysql]
    host = localhost
    port = 3306  # Optional, defaults to 3306
    user = your_mysql_user
    password = your_mysql_password
    database = your_database_name
    ```

    **Note:** Ensure the MySQL user specified has the necessary privileges to perform the actions you intend to execute.

### Usage

Run the script with the following command, specifying the path to your configuration file:

```bash
python mcp-mysql-server.py --config config.ini
```

The script exposes the following tools that you can use to interact with your MySQL database:

- `test_connection`: Tests the connection to the database and returns server information.
- `list_tables`: Lists all tables in the current database.
- `read_table`: Reads and returns all data from a specified table.
- `write_table`: Inserts a new row of data into a specified table.
- `get_table_schema`: Returns the schema (column definitions) for a specified table.
- `execute_sql`: Executes a custom SQL query and returns the results.

## Project Structure

- `mcp-mysql-server.py`: Main script containing the MySQL MCP server implementation
- `config.ini`: Configuration file for MySQL connection parameters
- `requirements.txt`: List of Python dependencies
- `changes.log`: Log of changes made to the project

## Docker Support

This project can be run in Docker containers using Docker Compose. The setup includes:

1. A MySQL container with sample data
2. The MCP MySQL Server container

### Running with Docker

1. Make sure you have Docker and Docker Compose installed on your system.
2. Clone this repository.
3. From the repository root, run:

```bash
docker-compose up -d
```

This will:
- Start a MySQL server with sample data (users and posts tables)
- Start the MCP MySQL Server connected to the MySQL database

### Configuration for Docker

A special configuration file (`config.docker.ini`) is used when running in Docker, which points to the MySQL container.

## Testing

Unit tests are provided to ensure the functionality works correctly. The tests use mocking to avoid requiring an actual database connection.

### Running Tests Locally

```bash
# Make a copy of the main script with underscore naming
cp mcp-mysql-server.py mcp_mysql_server.py

# Run the tests
python -m unittest tests.py
```

### Running Tests with Docker

```bash
docker-compose -f docker-compose.test.yml up --build
```

This will build a test container and run the unit tests within it.

## Development

For developers who want to extend this tool, you can add new functionalities by creating additional MCP tools. Each tool is a Python function decorated with `@mcp.tool()` that handles a specific database operation.

Example of adding a new tool:

```python
@mcp.tool()
def my_new_tool(param1: str, param2: int) -> dict:
    """
    Documentation for the new tool.
    """
    connection = create_mysql_connection()
    cursor = connection.cursor()
    try:
        # Your tool implementation here
        return {"result": "success"}
    finally:
        cursor.close()
        connection.close()
```
