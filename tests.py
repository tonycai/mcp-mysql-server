import unittest
from unittest.mock import patch, MagicMock
import json
import configparser
import mysql.connector
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the main module
import mcp_mysql_server

class TestMCPMySQLServer(unittest.TestCase):
    @patch('mcp_mysql_server.create_mysql_connection')
    def test_test_connection(self, mock_connection):
        # Mock the connection
        mock_conn = MagicMock()
        mock_conn.is_connected.return_value = True
        mock_conn.get_server_info.return_value = "8.0.28"
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ["test_db"]
        mock_conn.cursor.return_value = mock_cursor
        mock_connection.return_value = mock_conn

        # Call the function
        result = mcp_mysql_server.test_connection()
        
        # Verify the result
        self.assertEqual(result["status"], "Connected")
        self.assertEqual(result["server_version"], "8.0.28")
        self.assertEqual(result["database"], "test_db")
        
        # Verify that the cursor was closed
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('mcp_mysql_server.create_mysql_connection')
    def test_list_tables(self, mock_connection):
        # Mock the connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [("users",), ("posts",)]
        mock_conn.cursor.return_value = mock_cursor
        mock_connection.return_value = mock_conn

        # Call the function
        result = mcp_mysql_server.list_tables()
        
        # Verify the result
        self.assertEqual(result["tables"], ["users", "posts"])
        
        # Verify that the cursor was closed
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('mcp_mysql_server.create_mysql_connection')
    def test_read_table(self, mock_connection):
        # Mock the connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {"id": 1, "username": "user1", "email": "user1@example.com"},
            {"id": 2, "username": "user2", "email": "user2@example.com"}
        ]
        mock_conn.cursor.return_value = mock_cursor
        mock_connection.return_value = mock_conn

        # Call the function
        result = mcp_mysql_server.read_table("users")
        
        # Verify the result
        self.assertEqual(len(result["data"]), 2)
        self.assertEqual(result["data"][0]["username"], "user1")
        self.assertEqual(result["data"][1]["email"], "user2@example.com")
        
        # Verify the SQL execution
        mock_cursor.execute.assert_called_with("SELECT * FROM users")
        
        # Verify that the cursor was closed
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('mcp_mysql_server.create_mysql_connection')
    def test_get_table_schema(self, mock_connection):
        # Mock the connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            ("id", "int(11)", "NO", "PRI", None, "auto_increment"),
            ("username", "varchar(50)", "NO", "UNI", None, "")
        ]
        mock_conn.cursor.return_value = mock_cursor
        mock_connection.return_value = mock_conn

        # Call the function
        result = mcp_mysql_server.get_table_schema("users")
        
        # Verify the result
        self.assertEqual(len(result["schema"]), 2)
        self.assertEqual(result["schema"][0]["Field"], "id")
        self.assertEqual(result["schema"][0]["Type"], "int(11)")
        self.assertEqual(result["schema"][1]["Field"], "username")
        self.assertEqual(result["schema"][1]["Key"], "UNI")
        
        # Verify the SQL execution
        mock_cursor.execute.assert_called_with("DESCRIBE users")
        
        # Verify that the cursor was closed
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('mcp_mysql_server.create_mysql_connection')
    def test_write_table(self, mock_connection):
        # Mock the connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connection.return_value = mock_conn

        # Data to insert
        data = {"username": "new_user", "email": "new_user@example.com"}

        # Call the function
        result = mcp_mysql_server.write_table("users", data)
        
        # Verify the result
        self.assertEqual(result, "Data inserted successfully.")
        
        # Verify that commit was called
        mock_conn.commit.assert_called_once()
        
        # Verify that the cursor was closed
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('mcp_mysql_server.create_mysql_connection')
    def test_execute_sql_select(self, mock_connection):
        # Mock the connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {"id": 1, "username": "user1"},
            {"id": 2, "username": "user2"}
        ]
        mock_conn.cursor.return_value = mock_cursor
        mock_connection.return_value = mock_conn

        # Call the function with a SELECT query
        result = mcp_mysql_server.execute_sql("SELECT id, username FROM users")
        
        # Verify the result
        self.assertEqual(len(result["data"]), 2)
        self.assertEqual(result["data"][0]["username"], "user1")
        
        # Verify the SQL execution
        mock_cursor.execute.assert_called_with("SELECT id, username FROM users")
        
        # Verify that the cursor was closed
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('mcp_mysql_server.create_mysql_connection')
    def test_execute_sql_insert(self, mock_connection):
        # Mock the connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connection.return_value = mock_conn

        # Call the function with an INSERT query
        result = mcp_mysql_server.execute_sql("INSERT INTO users (username, email) VALUES ('test', 'test@example.com')")
        
        # Verify the result
        self.assertEqual(result["status"], "Query executed successfully.")
        
        # Verify that commit was called
        mock_conn.commit.assert_called_once()
        
        # Verify that the cursor was closed
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()