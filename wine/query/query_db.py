import sqlite3
from typing import List, Any
import pandas as pd


def query_one_result(wine_id: str, db='systemet.db'):
    con = sqlite3.connect('./wine/systemet.db')
    query_str = "SELECT * FROM main.systembolaget WHERE id = {}".format(int(wine_id))
    return pd.read_sql_query(query_str, con).to_dict('records')[0]

    # for row in cur.execute(query_str):
    #    row_dict = dict(zip([i[0] for i in cur.description], row))  # Convert the row tuple to a dictionary
    #    return row_dict


def query_sql(index_result: List, db='./systemet.db') -> List[Any]:
    con = sqlite3.connect('./wine/systemet.db')
    ids = []
    for res in index_result:
        ids.append(str(res['id']))

    query_str = "SELECT * FROM systembolaget WHERE id IN ({}) " \
                "AND images is not '[]' " \
        .format(', '.join(ids))  # Changed the query to use placeholders

    print("Query String: " + query_str)  # Added line to print query_str

    df = pd.read_sql_query(query_str, con)

    # Definiera ditt reguljära uttryck och funktionen för att modifiera URL:en
    regex = "(?P<url>https?://[^\\s]+)"

    def modify_url(url):
        return url[:-2] + "_400.png?q=75&w=2000"

    # Extrahera matchningen från kolumnen images och applicera funktionen
    df['image_compiled'] = df['images'].str.extract(regex, expand=False).apply(modify_url)

    return df.to_dict('records')
