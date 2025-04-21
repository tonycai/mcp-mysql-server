#!/bin/bash

# Rename the main script to match the import in the test file
cp mcp-mysql-server.py mcp_mysql_server.py

# Run the tests
python -m unittest tests.py