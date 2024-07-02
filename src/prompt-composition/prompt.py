import os

from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from openai import APIConnectionError
from openai import AuthenticationError
from langchain_core.prompts import PromptTemplate
 

def prompt_composition():
    try:
        prompt_template = "Tell me a {adjective} joke"
        prompt = PromptTemplate(
            input_variables=["adjective"], template=prompt_template
        )
        llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT"),
        openai_api_version=os.getenv("OPENAI_API_VERSION"),
        model_version="0301"
        )
        chain = prompt | llm

        response = chain.invoke("your adjective here")
        print(response.content)

    except APIConnectionError as ApiError:
        print(f"An error occured connecting to Azure Open AI. Error: {ApiError.message}")
    except AuthenticationError as AuthError:
        print(f"An error occured whilst authenticating to Azure Open AI: {AuthError.message}")

if __name__ == "__main__":
    load_dotenv()
    prompt_composition()