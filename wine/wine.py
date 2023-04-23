import operator

import streamlit as st

from query.query_db import query_sql, query_one_result
from query.querysvbertwine import query_swe_bert
from wine_data_collect.preparedata import to_description

if 'query_text' not in st.session_state:
    print("I cool")
    st.session_state['query_text'] = "rödvin som smakar vanilj."


def load_data(q):
    result = query_swe_bert(q)
    wd = query_sql(result)
    for data in wd:
        for idx in result:
            if idx['id'] == data['id']:
                data['distance'] = idx['distance']

    return sorted(wd, key=operator.itemgetter('distance'), reverse=True)


def display_wine(wine, image_url):
    cols = st.columns([3, 3, 3])

    cols[0].image(image_url, width=100, use_column_width=False)

    with cols[1]:
        st.write(f"****{wine['productNameBold'].strip()}****")
        if wine['productNameThin'] != 'None':
            st.write(f"***{wine['productNameThin'].strip()}***")
        if wine['taste'] != "None":
            st.write(f"*{wine['taste'].strip()}*")
            st.write(f"**{wine['price']} kronor**")
    with cols[2]:
        has_button_clicked = st.button("Hitta liknande", key=image_url)
        if has_button_clicked:
            st.session_state['query_text'] = to_description(query_one_result(wine['id']))
            st.experimental_rerun()
        formatted_percentage = f"{wine['distance'] * 100:.2f}%"
        st.write(f"*match {formatted_percentage}*")

    st.write("---")


def display_wines(wine_data):
    for wine in wine_data:
        image_url = wine['image_compiled']
        display_wine(wine, image_url)


# Add a sidebar input for updating the query text
with st.sidebar:
    st.header("Semantisk sök")
    new_query_text = st.text_input("Sök i en mening vilken smak du letar efter:", value=st.session_state['query_text'])
    if new_query_text != st.session_state['query_text']:
        st.session_state['query_text'] = new_query_text
        st.experimental_rerun()

wine_data = load_data(st.session_state['query_text'])
image_urls = [data['image_compiled'] for data in wine_data]

st.title('Dryckesvis')
st.write(f'*Query: "{st.session_state["query_text"]}"*')
st.write("---")

display_wines(wine_data)
