from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from typing import cast

import chainlit as cl
import os

@cl.on_chat_start
async def on_chat_start():

    model = AzureChatOpenAI(
            deployment_name="gpt-35-turbo-16k",
            temperature=0.0,
            max_tokens=100
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You're a very knowledgeable historian who provides accurate and eloquent answers to historical questions.",
            ),
            ("human", "{question}"),
        ]
    )
    llm_chain = prompt | model | StrOutputParser()
    cl.user_session.set("chain", llm_chain)


@cl.on_message
async def on_message(message: cl.Message):
    llm_chain = cast(Runnable, cl.user_session.get("chain"))  # type: Runnable

    msg = cl.Message(content="")

    async for chunk in llm_chain.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()
