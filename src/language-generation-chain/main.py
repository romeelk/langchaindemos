import os

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from openai import  APIConnectionError
from openai import AuthenticationError
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

def print_pythoncode():
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT"),
        openai_api_version=os.getenv("OPENAI_API_VERSION"),
        model_version="0613"
    )

    
    try:
        prompt = ChatPromptTemplate.from_template("Write a short language function using {language} that will descirbe task {task}")
   
        code_chain = prompt | llm | StrOutputParser()
      
        test_prompt = ChatPromptTemplate.from_template("Write a unit test for {code}")

        composed_chain = {"code": code_chain} | test_prompt | llm | StrOutputParser()

        response = composed_chain.invoke({"language": "python",
                                "task":"print numbers 1 to 10"})
       
        print(response)
    except APIConnectionError as ApiError:
        print(f"An error occured when connecting to Azure Open AI. Error:{ApiError.message}")
    except AuthenticationError as AuthError:
        print(f"An error occured whilst authenticating to Azure Open AI: {AuthError.message}")

if __name__ == "__main__":
    load_dotenv()
    print("Langchain chain example")
    print_pythoncode()