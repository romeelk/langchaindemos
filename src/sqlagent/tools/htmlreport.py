from pydantic import BaseModel
from langchain_core.tools import StructuredTool, tool


   
@tool
def write_html_report(filename: str, html_template: str):
    """
        Writes a html report to disk

        Args:
            filename (str): The filename.
            html_template (str): The html_template.

        Returns:
            none
    """
    with open(filename, "w") as file:
        file.write(html_template)

class WriteReportArgsSchema(BaseModel):
    filename: str
    html_template: str

write_html_report_tool  = StructuredTool.from_function(func=write_html_report,name="write_html_report", description="Write HTML to disk.Use this tool whenever someone asks for a report", args_schema=WriteReportArgsSchema)