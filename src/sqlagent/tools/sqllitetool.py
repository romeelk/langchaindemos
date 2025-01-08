import sqlite3
from pydantic import BaseModel
from langchain_core.tools import BaseTool, tool

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

@tool
def describe_tables(table_names: str) -> str:
    """
    Lists sqllite tables 
    Args:
        table_names (str): The table_names.

    Returns:
        str: A list of tables
    """
    conn = sqlite3.connect('db.sqlite')
    tables = ','.join("'" + table_name + "'" for table_name in table_names.split(","))
    rows = conn.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name IN ({tables})").fetchall()
    return '\n'.join([row[0] for row in rows if row[0] is not None])