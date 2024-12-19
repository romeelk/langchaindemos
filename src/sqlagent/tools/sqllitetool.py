import sqlite3
from pydantic import BaseModel
from langchain_core.tools import BaseTool

conn = sqlite3.connect('db.sqlite')

def list_tables():
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = cursor.fetchall()
    return "\n".join([row[0] for row in rows if row[0] is not None])

# Define a custom tool
class SqlLiteTool(BaseTool):
    name: str = "run_sql_lite_query"
    description: str = "Run a query on a SQL lite database"
    def _run(self, query: str) -> str:
        """Use the tool."""
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except sqlite3.OperationalError as e:
            return f"The following error occured: {e}"
       

    async def _arun(self, query: str) -> str:
        """Use the tool."""
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows