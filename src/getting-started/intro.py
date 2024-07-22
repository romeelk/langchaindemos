import os

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from openai import  APIConnectionError
from openai import AuthenticationError


def getting_started():
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT"),
        openai_api_version=os.getenv("OPENAI_API_VERSION")
    )

    message = HumanMessage(
        content="Translate this sentence from English to French. My age is 10 years."
    )

    print(message)

    try:
        response = llm([message])
        print(response.content)
    except APIConnectionError as ApiError:
        print(f"An error occured when connecting to Azure Open AI. Error:{ApiError.message}")
    except AuthenticationError as AuthError:
        print(f"An error occured whilst authenticating to Azure Open AI: {AuthError.message}")

if __name__ == "__main__":
    load_dotenv()
    getting_started()