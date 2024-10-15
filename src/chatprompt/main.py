from langchain_core.prompts import (
    ChatPromptTemplate
)
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt  = ChatPromptTemplate.from_messages([
    ("system", "You are a world class technical documentation writer."),
    ("user", "{input}")
])

chain = prompt | llm | StrOutputParser()

response = chain.invoke({"input": "how can langsmith help with testing?"})

print(response)