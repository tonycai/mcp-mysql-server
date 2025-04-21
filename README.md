# mcp-mysql-server

A simple Python script for interacting with a local MySQL database via standard input/output (stdio).

## Overview

`mcp-mysql-server` provides a command-line interface for querying and inspecting the schema of a local MySQL database. It is designed for ease of use in local development environments where a lightweight, script-based interaction is preferred. The script utilizes standard input and output for commands and results, making it easy to integrate with other command-line tools and workflows.

## Features

* **Query Execution:** Execute SQL SELECT statements and view the results in a simple, readable format.
* **Schema Inspection:** Retrieve information about the database schema, including:
    * Listing all tables.
    * Displaying the columns and their data types for a specific table.
* **Configurable Access Controls:** Define connection parameters (host, user, password, database) through configuration, allowing secure access to the database.
* **stdio Interface:** Interact with the script using standard input for commands and receive output via standard output, facilitating scripting and automation.
* **Local Deployment Focus:** Optimized for use within local development environments.

## Getting Started

### Prerequisites

* Python 3.x installed on your system.
* A local MySQL server instance running.
* A Python MySQL connector library installed (e.g., `mysql-connector-python`). You can install it using pip:
    ```bash
    pip install mysql-connector-python
    ```

### Installation

1.  Download or clone the `mcp-mysql-server.py` script to your local machine.

### Configuration

1.  Create a configuration file (e.g., `config.ini`) in the same directory as the script or specify the path when running the script. The configuration file should have the following format:

    ```ini
    [mysql]
    host = localhost
    user = your_mysql_user
    password = your_mysql_password
    database = your_database_name
    ```

    **Note:** Ensure the MySQL user specified has the necessary privileges to perform the actions you intend to execute.

### Usage

You can interact with the `mcp-mysql-server.py` script by piping commands to it via standard input.

**Basic Syntax:**

```bash
echo "<command>" | python mcp-mysql-server.py --config config.ini
