import os

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.llms import AzureOpenAI

env_vars = ["AZURE_OPENAI_API_KEY","AZURE_OPENAI_ENDPOINT","OPENAI_API_VERSION"]

def load_env_settings() -> bool:
    keys_found = True
    for var in env_vars:
        if var in os.environ:
            print(f"Checking for Azure Open AI env vars: Found matching key {var}")
        else:
            keys_found = False
            break
    return keys_found

result = load_env_settings()

if(result == False):
    print("Could not load Azure Open AI settings from environmnt vars")
    for env_var in env_vars:
        print(f'Make sure the following env vars are set {env_var}')
else:
    quit()

llm = AzureChatOpenAI(
    azure_deployment="gpt4",
    openai_api_version="2023-05-15",
)

message = HumanMessage(
    content="Translate this sentence from English to French. My age is 10 years."
)
response = llm.invoke([message])

print(response.content)