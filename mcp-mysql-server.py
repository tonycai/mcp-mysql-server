import mysql.connector
from mysql.connector import Error
#from mcp import FastMCP
from fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("MySQL MCP Server")

# Establish connection to MySQL
def create_mysql_connection():
    try:
        connection = mysql.connector.connect(
            host="MySQL_Host_Address",  # Change to your MySQL host
            port=3306,         # Default MySQL port
            user="YourUsername",       # Replace with your MySQL username
            password="YourPassword",  # Replace with your MySQL password
            database="example_db"   # Replace with your MySQL database
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
        schema = [{"Field": row, "Type": row[1], "Null": row[2], "Key": row[3], "Default": row[4], "Extra": row[5]} for row in cursor.fetchall()]
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

# Start the MCP server
if __name__ == "__main__":
    mcp.run()
