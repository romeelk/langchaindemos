from langchain_openai import AzureChatOpenAI
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.prompts.chat import MessagesPlaceholder
import os
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# based on: https://python.langchain.com/v0.1/docs/expression_language/how_to/message_history/
load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT"),
    openai_api_version=os.getenv("OPENAI_API_VERSION"),
    model_version="0301",   
)   
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


prompt = ChatPromptTemplate(input_variables=["content"],
                            messages=[MessagesPlaceholder(variable_name="messages"),
                                HumanMessagePromptTemplate.from_template("{content}")])

runnable = prompt | llm 

with_message_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="content",
    history_messages_key="messages",
)

while True:
    content = input("input>>")
    response = with_message_history.invoke({"content":content}, config={"configurable": {"session_id": "abc123"}})
    print(response.content)