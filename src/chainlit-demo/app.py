from dotenv import load_dotenv
import os
import chainlit as cl
from langchain_openai import AzureChatOpenAI
 
load_dotenv()


@cl.on_chat_start
def main():
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT"),
        openai_api_version=os.getenv("OPENAI_API_VERSION")
    )   
    return "Hello! I am a chatbot. How can I help you today?"