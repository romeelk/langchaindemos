from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from langchain.memory import ChatMessageHistory

load_dotenv()


city = "Tell me about city {city}"

prompt = PromptTemplate(
    input_variables=["city"],
    template=city,
)

description = "It is software dev firm specifically focusing on automation software"

llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT"),
    openai_api_version=os.getenv("OPENAI_API_VERSION"),
    model_version="0301",   
)   

chain = prompt | llm 

response = chain.invoke("New york")

print(response.content)

message_history = ChatMessageHistory()

message_history.add_user_message(response.content)

print("history-->" +str(message_history.messages))