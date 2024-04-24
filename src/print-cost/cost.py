import os

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv
from openai import APIConnectionError
from openai import AuthenticationError
from langchain.callbacks import get_openai_callback

load_dotenv()   

try:
    
    llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT"),
    openai_api_version=os.getenv("OPENAI_API_VERSION"),
    model_version="0301"
    )

    messages = [
        HumanMessage(
        content="I don't like LLMs"
    ),
        SystemMessage(content="Say the opposite of what I say")
    ]
    with get_openai_callback() as cb:
        response = llm.invoke(messages)
        print(
        f"Total Cost (USD): ${format(cb.total_cost, '.6f')}"
        )
        print(response.content)
        # without specifying the model version, flat-rate 0.002 USD per 1k input and output tokens is used
except APIConnectionError as ApiError:
    print(f"An error occured  connecting to Azure Open AI. Error: {ApiError.message}")
except AuthenticationError as AuthError:
    print(f"An error occured whilst authenticating to Azure Open AI: {AuthError.message}")