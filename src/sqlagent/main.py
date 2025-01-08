# Demo of a langchain sql agent to query a SQL lite database
# from tools.sqllitetool import CustomTool
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate
)
from langchain.agents import AgentExecutor, create_tool_calling_agent
from dotenv import load_dotenv
from tools.sqllitetool import SqlLiteTool,list_tables,describe_tables
from tools.htmlreport import write_html_report
from langchain.memory import ConversationBufferMemory
load_dotenv()

# list tables in sqllite database
tables = list_tables()
# Create an instance of the custom tool
custom_tool = SqlLiteTool()
describe_table_tool = describe_tables
# Define the language model
llm = ChatOpenAI()
# Define the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", f"You are a AI assistant who has access to a SQL lite database.\n{tables}"),
    ("system", f"The database has tables: {tables}"),
    ("system", "Do not make assumptions about what tables exist or what columns exist. use 'describes_table' function."),
    ("human", "{chat_history},{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# create chat history memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
# Create the agent
agent = create_tool_calling_agent(llm, [custom_tool,describe_tables, write_html_report], prompt)

# Create the AgentExecutor
agent_executor = AgentExecutor(agent=agent, tools=[custom_tool,describe_tables,write_html_report], memory=memory,verbose=True)

# Use the agent
result = agent_executor.invoke({"input": "List the databases?"})

result = agent_executor.invoke({"input": "Describe in users"})
result = agent_executor.invoke({"input": "select count(*) from users"})

result = agent_executor.invoke({"input": "select top 10 * from users"})

result = agent_executor.invoke({"input": "summarise the top 5 products. write the report to report.html"})

result = agent_executor.invoke({"input": "repeat the exact process for top 5 users"})
# Add memory to the agent
