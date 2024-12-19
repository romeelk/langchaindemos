# Demo of a langchain sql agent to query a SQL lite database
# from tools.sqllitetool import CustomTool
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate
)
from langchain.agents import AgentExecutor, create_tool_calling_agent
from dotenv import load_dotenv
from tools.sqllitetool import SqlLiteTool,list_tables

load_dotenv()

# list tables in sqllite database
tables = list_tables()
# Create an instance of the custom tool
custom_tool = SqlLiteTool()

# Define the language model
llm = ChatOpenAI()

# Define the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", f"You are a AI assistant who has access to a SQL lite database.\n{tables}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# Create the agent
agent = create_tool_calling_agent(llm, [custom_tool], prompt)

# Create the AgentExecutor
agent_executor = AgentExecutor(agent=agent, tools=[custom_tool], verbose=True)

# Use the agent
result = agent_executor.invoke({"input": "List the databases?"})

result = agent_executor.invoke({"input": "select count(*) from users"})

result = agent_executor.invoke({"input": "select top 10 * from users"})

result = agent_executor.invoke({"input": "select top 10 * from pakistan"})
print(result)
