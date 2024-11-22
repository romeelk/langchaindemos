# https://python.langchain.com/v0.2/docs/versions/migrating_chains/retrieval_qa/

import os
import getpass
import bs4
from langchain_community.document_loaders import WebBaseLoader
from dotenv import load_dotenv
import bs4
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate, HumanMessagePromptTemplate
)

os.environ["OPENAI_API_KEY"] = getpass.getpass(prompt="Enter OpenApi key:")

# use a cheaper model
llm = ChatOpenAI(model="gpt-4o-mini")

print("Langchain RAG demo")

print("Loading doc from web: https://lilianweng.github.io/posts/2023-06-23-agent/")

loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)

docs = loader.load()

print(f"Number of docs loaded: {len(docs)}")

# Use a splitter to chunk document into 1000 parts

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# split the document
splits = text_splitter.split_documents(docs)

print(f"Number of docs splits: {len(splits)}")

vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

prompt = ChatPromptTemplate(input_variables=["question","context"],
messages=[HumanMessagePromptTemplate.from_template("You are an assistant for \
                                                   question-answering tasks. \
                                                   Use the following pieces of \
                                                   retrieved context to answer \
                                                   the question. If you don't \
                                                   know the answer, just say \
                                                   that you don't know. Use \
                                                   three sentences maximum \
                                                   and keep the answer concise. \
                                                   Question: {question}.Context: {context}. Answer ")])

rag_chain = {"context": retriever | format_docs, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser()

response = rag_chain.invoke("What is task chain of thought")

print(response)