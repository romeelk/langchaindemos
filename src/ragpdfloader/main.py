import getpass
import os
import sys
from langchain_core.prompts import (
    ChatPromptTemplate, HumanMessagePromptTemplate
)
from langchain_community.document_loaders import PDFMinerLoader
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI


os.environ["OPENAI_API_KEY"] = getpass.getpass()
llm = ChatOpenAI(model="gpt-4o-mini")

print("Welcome to RAG PDF loader")

file_name = "python_cheat_sheet.pdf"
pdf_loader = PDFMinerLoader(file_name)

doc_list = pdf_loader.load()
print(f"Loading pdf file {file_name}")
print(f'Loaded {len(doc_list)} documents')

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

splits = text_splitter.split_documents(doc_list)

print(f"Number of docs splits: {len(splits)}")

# Use Chroma to store embeddings
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

prompt = ChatPromptTemplate(input_variables=["content","context"],
messages=[HumanMessagePromptTemplate.from_template("You are an assistant for \
                                                   question-answering tasks. \
                                                   Use the following pieces of \
                                                   retrieved context to answer \
                                                   the question. If you don't \
                                                   know the answer, just say \
                                                   that you don't know. Use \
                                                   three sentences maximum \
                                                   and keep the answer concise. \
                                                   Question: {content}.Context: {context}. Answer ")])


while True:
    content = input(">>")

    if content == "exit":
        sys.exit(0)
    rag_chain = {"context": retriever | format_docs, "content": RunnablePassthrough()} | prompt | llm | StrOutputParser()

    print(rag_chain.invoke(content))