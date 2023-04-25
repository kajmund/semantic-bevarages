import faiss
import pandas as pd
import streamlit as st
from sentence_transformers import SentenceTransformer


@st.cache_resource  # 👈 Add the caching decorator
def load_model():
    model_name = 'KBLab/sentence-bert-swedish-cased'
    return SentenceTransformer(model_name, device='cpu')


@st.cache_resource
def load_index():
    return faiss.read_index("./wine/wine_data_collect/wines.index")


# Ladda modell och index vid start
model = load_model()
index = load_index()


def search_FAISSIndex(data=None, id_col_name=None, query=None, index=None, nprobe=None, model=None, topk=20):
    # Convert the query into embeddings
    query_embedding = model.encode([query])[0]
    dim = query_embedding.shape[0]
    query_embedding = query_embedding.reshape(1, dim)

    # Normalize the Query Embedding
    faiss.normalize_L2(query_embedding)
    index.nprobe = nprobe

    D, I = index.search(query_embedding, topk)
    ids = [i for i in I][0]

    print(ids)
    inner_product = [d for d in D][0]

    search_result = pd.DataFrame()
    search_result["id"] = ids
    search_result['cosine_sim'] = inner_product

    if data is not None:
        dat = data[data[id_col_name].isin(ids)]
    else:
        dat = pd.DataFrame(ids, columns=[id_col_name])
    dat = pd.merge(dat, search_result, on=id_col_name)
    dat = dat.sort_values('cosine_sim', ascending=False)

    return dat


def query_swe_bert(query):
    print("Bert query:\n" + query)
    search_result = search_FAISSIndex(id_col_name="id", query=query, index=index, nprobe=10, model=model, topk=20)
    combined_list = []
    id_list = [id + 1 for id in search_result['id']]
    for distance, _ids in zip(search_result['cosine_sim'], id_list):
        combined_list.append({"distance": distance, "id": _ids})

    return combined_list
