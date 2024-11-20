
import os
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

print("Langchain basics. Legacy chain")

load_dotenv()
llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini")

prompt = PromptTemplate.from_template("Summarise the following {topic}.")

chain  = LLMChain(llm=llm,prompt=prompt)

response = chain.invoke(prompt.format(topic="Large Language Models"))
print(response['text'])
