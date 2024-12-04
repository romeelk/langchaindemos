from chromadb.utils import embedding_functions

default_ef = embedding_functions.DefaultEmbeddingFunction()

val = default_ef(["foo","shoe"])

print(val)

print(len(val))