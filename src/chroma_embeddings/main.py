
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from dotenv import load_dotenv 
from langchain_chroma import Chroma
load_dotenv()

# create AzureOpenAIEmbeddings to calculate embeddings
embeddings = AzureOpenAIEmbeddings()

# load the ext
text_loader = TextLoader("facts.txt")

# load the CharacterTextSplitter a split on new line
text_splitter = CharacterTextSplitter(separator="\n")

# Specify a split chunk size of 200 - This will split by 200 then find next new line
text_splitter._chunk_size = 200
text_splitter._chunk_overlap = 0

# load and chunk the text
docs = text_loader.load_and_split(text_splitter)

# Create Chromadb, and persist embeddings into 'emb' folder

db = Chroma.from_documents(docs, embedding=embeddings,persist_directory="emb")

# Do a similarity search
results = db.similarity_search_with_score("What is an interesting fact of the english language")

for result in results:
    print(f"Search score={result[1]}")
    print(f"Search response: {result[0]}")