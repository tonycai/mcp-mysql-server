FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create a non-root user to run the application
RUN useradd -m appuser
USER appuser

# Expose the MCP server port (if needed)
# EXPOSE 8000

# Run the MCP server
CMD ["python", "mcp-mysql-server.py", "--config", "config.ini"]