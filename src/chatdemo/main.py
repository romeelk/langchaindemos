from langchain_openai import AzureChatOpenAI
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import os
from dotenv import load_dotenv

load_dotenv()
prompt = ChatPromptTemplate(input_variables=["content"],
messages=[HumanMessagePromptTemplate.from_template("{content}")])


llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT"),
    openai_api_version=os.getenv("OPENAI_API_VERSION"),
    model_version="0301",
)

while True:
    content = input(">>")

    chain = prompt | llm | StrOutputParser()

    print(chain.invoke({"content":content}))

