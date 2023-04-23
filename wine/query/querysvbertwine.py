import math
import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer


## This function converts the L2_score into inner product def
def calculate_inner_product(L2_score):
    return (2 - math.pow(L2_score, 2)) / 2


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
    L2_score = [d for d in D][0]
    inner_product = [calculate_inner_product(l2) for l2 in L2_score]

    search_result = pd.DataFrame()
    search_result["id"] = ids
    search_result['cosine_sim'] = inner_product
    search_result['L2_score'] = L2_score

    if data is not None:
        dat = data[data[id_col_name].isin(ids)]
    else:
        dat = pd.DataFrame(ids, columns=[id_col_name])
    dat = pd.merge(dat, search_result, on=id_col_name)
    dat = dat.sort_values('cosine_sim', ascending=False)

    return dat


def query_swe_bert(query):
    print("Bert query:\n" + query)
    index = faiss.read_index("./wine/wine_data_collect/movies_desc.index")
    # from wine_data_collect import preparedata
    # vinbeskrivningar = preparedata.collect_all_sentences()
    model_name = 'KBLab/sentence-bert-swedish-cased'
    model = SentenceTransformer(model_name)
    # query = "drycken heter crémant d'alsace chardonnay. denna dryck smakar fruktig, mycket frisk, nyanserad smak med inslag av päron, gula äpplen, rostat bröd, honungsmelon och grapefrukt..den säljs buteljerad på flaska. drycken har en organisk klassificering 1.drycken har en alkoholprocent på 12.5%. drycken har en volym på 375 ml. dryckens pris är 99.0. drycken kommer från landet frankrike. drycken är av kategorin mousserande vin och underkategorin torrt vitt. drycken rekommenderas serveras serveras vid 8-10°c som aperitif, eller till rätter av fisk eller skaldjur, eller till sallader..den passar som eller till aperitif, fisk, skaldjur, grönsaker. drycken har förslutits genom naturkork.druvorna är gjort på druvornachardonnay..dryckens färgton är ljusgul färg.. per 100 milliliter är sockermängden 0.9"
    # print(query)
    search_result = search_FAISSIndex( id_col_name="id", query=query, index=index, nprobe=10, model=model, topk=20)
    # search_result = search_result[['id', vinbeskrivning', 'cosine_sim', 'L2_score']]
    # print(search_result)
    combined_list = []
    id_list = [id + 1 for id in search_result['id']]
    for distance, _ids in zip(search_result['cosine_sim'], id_list):
        combined_list.append({"distance": distance, "id": _ids})

    return combined_list
