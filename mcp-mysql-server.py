import mysql.connector
from mysql.connector import Error
import configparser
import argparse
import sys
#from mcp import FastMCP
from fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("MySQL MCP Server")

# Parse command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='MySQL MCP Server')
    parser.add_argument('--config', type=str, default='config.ini', help='Path to the configuration file')
    return parser.parse_args()

# Load configuration
def load_config(config_file):
    config = configparser.ConfigParser()
    try:
        config.read(config_file)
        return {
            'host': config['mysql']['host'],
            'port': int(config['mysql'].get('port', '3306')),
            'user': config['mysql']['user'],
            'password': config['mysql']['password'],
            'database': config['mysql']['database']
        }
    except Exception as e:
        print(f"Error loading configuration: {e}")
        sys.exit(1)

# Configuration
args = parse_arguments()
db_config = load_config(args.config)

# Establish connection to MySQL
def create_mysql_connection():
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        raise

# Tool: Read data from a table
@mcp.tool()
def read_table(table_name: str) -> dict:
    """
    Reads data from the specified table and returns it.
    """
    connection = create_mysql_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()
        return {"data": rows}
    finally:
        cursor.close()
        connection.close()

# Tool: Write data to a table
@mcp.tool()
def write_table(table_name: str, data: dict) -> str:
    """
    Writes a row of data to the specified table.
    """
    connection = create_mysql_connection()
    cursor = connection.cursor()
    try:
        # Generate SQL for INSERT
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        cursor.execute(query, tuple(data.values()))
        connection.commit()
        return "Data inserted successfully."
    except Exception as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        connection.close()

# Tool: Get schema of a table
@mcp.tool()
def get_table_schema(table_name: str) -> dict:
    """
    Fetches the schema of the specified table.
    """
    connection = create_mysql_connection()
    cursor = connection.cursor()
    try:
        query = f"DESCRIBE {table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()
        schema = []
        for row in rows:
            schema.append({
                "Field": row[0],
                "Type": row[1],
                "Null": row[2],
                "Key": row[3],
                "Default": row[4],
                "Extra": row[5]
            })
        return {"schema": schema}
    finally:
        cursor.close()
        connection.close()

# Tool: Execute custom SQL query
@mcp.tool()
def execute_sql(query: str) -> dict:
    """
    Executes a custom SQL query and returns the result.
    """
    connection = create_mysql_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query)
        # Check if it's a SELECT query
        if query.strip().lower().startswith("select"):
            rows = cursor.fetchall()
            return {"data": rows}
        else:
            connection.commit()
            return {"status": "Query executed successfully."}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()

# Tool: List all tables
@mcp.tool()
def list_tables() -> dict:
    """
    Lists all tables in the database.
    """
    connection = create_mysql_connection()
    cursor = connection.cursor()
    try:
        query = "SHOW TABLES"
        cursor.execute(query)
        tables = [row[0] for row in cursor.fetchall()]
        return {"tables": tables}
    finally:
        cursor.close()
        connection.close()

# Tool: Test connection
@mcp.tool()
def test_connection() -> dict:
    """
    Tests the database connection and returns server information.
    """
    try:
        connection = create_mysql_connection()
        if connection.is_connected():
            db_info = connection.get_server_info()
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE()")
            database_name = cursor.fetchone()[0]
            cursor.close()
            connection.close()
            return {
                "status": "Connected",
                "server_version": db_info,
                "database": database_name
            }
    except Error as e:
        return {"status": "Failed", "error": str(e)}

# Start the MCP server
if __name__ == "__main__":
    mcp.run()
