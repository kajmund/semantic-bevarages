from sentence_transformers import SentenceTransformer
import faiss
import openai
import numpy as np

openai.api_key = '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'



def query_index(query: str, embeddings='./import/embeddings.index'):
    text_model = SentenceTransformer('sentence-transformers/clip-ViT-B-32-multilingual-v1')
    index = faiss.read_index(embeddings)
    target_vector = text_model.encode(sentences=[query])
    distances, nearest_indexes = index.search(target_vector, 15)

    combined_list = []
    for distance, index in zip(distances[0], nearest_indexes[0]):
        combined_list.append({"distance": distance, "id": index})

    return combined_list


def query_ada(query: str, embeddings='./import/ada_system.index'):
    emb = openai.Embedding.create(input=query, engine="text-embedding-ada-002")
    result = emb.data[0].embedding
    query_vector = np.array(result)
    k = 10
    # distances, indexes
    combined_list = []
    index = faiss.read_index(embeddings)
    distances, nearest_indexes = index.search(query_vector.reshape(1, -1), k)
    for distance, ids in zip(distances[0], nearest_indexes[0]):
        combined_list.append({"distance": distance, "id": ids})

    return combined_list

# r = query_ada('Äpple och kanel', embeddings='../import/embeddings_ada2.index')
