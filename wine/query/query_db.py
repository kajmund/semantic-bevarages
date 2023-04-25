import sqlite3
from typing import List, Any
import pandas as pd
import streamlit as st
import contextlib

DB_PATH = './wine/systemet.db'


@contextlib.contextmanager
def connect_to_db(db_path):
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()


def query_one_result(wine_id: str):
    query_str = "SELECT * FROM main.systembolaget WHERE id = {}".format(int(wine_id))
    with connect_to_db(DB_PATH) as con:
        return pd.read_sql_query(query_str, con).to_dict('records')[0]


def query_sql(index_result: List) -> List[Any]:
    ids = []
    for res in index_result:
        ids.append(str(res['id']))

    query_str = "SELECT * FROM systembolaget WHERE id IN ({}) " \
                "AND images is not '[]' " \
        .format(', '.join(ids))

    print("Query String: " + query_str)

    with connect_to_db(DB_PATH) as con:
        df = pd.read_sql_query(query_str, con)

    regex = "(?P<url>https?://[^\\s]+)"

    def modify_url(url):
        return url[:-2] + "_400.png?q=75&w=2000"

    df['image_compiled'] = df['images'].str.extract(regex, expand=False).apply(modify_url)

    return df.to_dict('records')
