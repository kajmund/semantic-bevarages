import sqlite3
import pandas as pd


def to_description(row) -> str:
    def safe_str(value, prefix="", suffix=""):
        return prefix + str(value) + suffix if value not in ("None", "") else ""

    template = (
        "Drycken heter {productNameBold}{productNameThin}. "
        "{taste_desc}"
        "Den säljs buteljerad på {bottleText}. "
        "{organic_desc}"
        "Drycken har en alkoholprocent på {alcoholPercentage}%. "
        "Drycken har en volym på {volumeText}. "
        "Dryckens pris är {price} kr."
        "Drycken kommer från landet {country}."
        "Drycken är av kategorin {categoryLevel2} och underkategorin {categoryLevel3}."
        "{usage_desc}"
        "{tasteSymbols}"
        "{seal_desc}"
        "{vintage_desc}"
        "{grapes}"
        "Dryckens färgton är {color}"
        "Per 100 milliliter är sockermängden {sugarContentGramPer100ml}."
    )

    description = template.format(
        productNameBold=row['productNameBold'],
        productNameThin=safe_str(row['productNameThin'], " "),
        taste_desc=safe_str(row['taste'], "Denna dryck smakar ", ""),
        bottleText=row['bottleText'],
        organic_desc="Drycken har en organisk klassificering " + safe_str(row['isOrganic'], "", ". ") if row[
                                                                                                             'isOrganic'] == 1 else "",
        alcoholPercentage=row['alcoholPercentage'],
        volumeText=row['volumeText'],
        price=row['price'],
        country=row['country'],
        categoryLevel2=row['categoryLevel2'],
        categoryLevel3=row['categoryLevel3'],
        usage_desc=safe_str(row['usage'], "Dryckens användningsområde:  ", ""),
        tasteSymbols=safe_str(row['tasteSymbols'], "Den passar som eller till", "."),
        seal_desc=safe_str(row['seal'], "Drycken har förslutits genom ", "."),
        vintage_desc=safe_str(row['vintage'], "Den har en årgång av ", "."),
        grapes=safe_str(row['grapes'], "Druvorna som drycken är tillverkad av är ", "."),
        color=row['color'],
        sugarContentGramPer100ml=row['sugarContentGramPer100ml'],
    )

    return description.strip().lower()


def collect_all_sentences(limit=-1, db='../systemet.db'):
    texts = []
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if limit == -1:
        cur.execute("SELECT * FROM systembolaget")
    else:
        cur.execute("SELECT * FROM systembolaget limit " + str(limit))

    rows = cur.fetchall()
    for row in rows:
        texts.append(to_description(row))
    vinbeskrivningar = pd.DataFrame(texts, columns=['vinbeskrivning'])
    vinbeskrivningar['id'] = vinbeskrivningar.index

    print(vinbeskrivningar.head(2))
    return vinbeskrivningar

