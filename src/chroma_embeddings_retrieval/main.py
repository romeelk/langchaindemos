import os
from dotenv import load_dotenv
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()
llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT"),
    model_version="2024-07-18"
    )

db = Chroma.from_texts(["harrison worked at kensho", "bears like to eat honey","Tom worked in London","Tom is an AI Consultant"],
    embedding=AzureOpenAIEmbeddings(),)

retriever = db.as_retriever()

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
output_parser = StrOutputParser()

setup_and_retrieval = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}
)
chain = setup_and_retrieval | prompt | llm | output_parser

response = chain.invoke("What is toms job?")

print(response)

response = chain.invoke("What about Harrirson?")

print(response)
