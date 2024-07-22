
import openai
import os
from langchain import OpenAI

print("Langchain basics")
from dotenv import load_dotenv


load_dotenv()
llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))

result = llm.invoke("What is Open AI?")

print(result)