import os
import argparse

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from openai import APIConnectionError
from openai import AuthenticationError
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


def print_pythoncode(args):

    print(args.task)
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT"),
        openai_api_version=os.getenv("OPENAI_API_VERSION"),
        model_version="0613",
        temperature=0.0
    )
    try:
        prompt = ChatPromptTemplate.from_template("Write a short language function using {language} that will describe task {task}")
   
        code_chain = prompt | llm | {"code:" :StrOutputParser()}

        test_prompt = ChatPromptTemplate.from_template("Write a unit test for {code}")

        composed_chain = {"code": code_chain} | test_prompt | llm | StrOutputParser()

        response = composed_chain.invoke({"language": args.language,
                                "task":args.task})
       
        print(response)

    except APIConnectionError as ApiError:
        print(f"An error occured when connecting to Azure Open AI. Error:{ApiError.message}")
    except AuthenticationError as AuthError:
        print(f"An error occured whilst authenticating to Azure Open AI: {AuthError.message}")

def parse_cmd_line_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--language", default="python")
    parser.add_argument("--task", default="return a list of numbers")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    load_dotenv()
    print("Langchain chain example")
    args = parse_cmd_line_args()
  
    print_pythoncode(args)