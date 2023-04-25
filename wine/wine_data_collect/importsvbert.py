from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import preparedata

data = preparedata.collect_all_sentences()
vinbeskrivningar = data['vinbeskrivning'].tolist()
ids = data['id'].tolist()
ids = np.array(ids)

# Ladda in en transformer-modell och dess tokenizer
model_name = 'KBLab/sentence-bert-swedish-cased'
model = SentenceTransformer(model_name)

## Before we train the embeddings, we will normalise the Embeddings
embeddings = model.encode(vinbeskrivningar)  ## Extract the sentenceembeddings

dim = 768  ## Embedding Dimension
ncentroids = 50  ## This is a hyperparameter, and indicates number of clusters to be split into
m = 16  ## This is also a hyper parameter indicating number chunks the embeddings must be divided into
quantiser = faiss.IndexFlatL2(dim)
index = faiss.IndexIVFPQ(quantiser, dim, ncentroids, m, 8)
## Before we train the embeddings, we will normalise the Embeddings
faiss.normalize_L2(embeddings)

index.train(embeddings)  ## This step, will do the clustering and create the clusters for each chunk
print(index.is_trained)  ## Will print true if the index has been trained (The cluster centroids have been identified)
faiss.write_index(index, "trained.index")  ## The trained.index contains the details about the cluster centroids.

index.add_with_ids(embeddings, ids)
print("Total Number of Embeddings in the index", index.ntotal)
faiss.write_index(index, "wines.index")
