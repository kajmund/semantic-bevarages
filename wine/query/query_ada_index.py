# Load the FAISS index from disk.
import pickle

import numpy as np
import openai
from langchain import VectorDBQAWithSourcesChain, OpenAI, FAISS
import faiss
import os

from langchain.embeddings import OpenAIEmbeddings

os.environ["OPENAI_API_KEY"] = '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'

index = faiss.read_index("../import/ada_system.index")

# Load the vector store from disk.
#with open("../import/cloudflare_docs.pkl", "rb") as f:
#    store = pickle.load(f)

# merge the index and store
#store.index = index


emb = openai.Embedding.create(input=query, engine="text-embedding-ada-002")
result = emb.data[0].embedding
query_vector = np.array(result)
print(result)
k = 10
D, I = index.search(result, k)

print(D, I)
