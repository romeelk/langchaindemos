
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv 

load_dotenv()

text_loader = TextLoader("facts.txt")

text_splitter = CharacterTextSplitter(separator="\n")

text_splitter._chunk_size = 200
text_splitter._chunk_overlap = 0


docs = text_loader.load_and_split(text_splitter)

for chunk in docs:
    print(chunk.page_content)
    print("\n")

embeddings = OpenAIEmbeddings()

query = "Tell me about geography"

response = embeddings.embed_query(query)

print(response)

print(f"Total dimensions: {len(response)})")