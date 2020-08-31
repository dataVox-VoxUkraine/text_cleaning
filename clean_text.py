import pandas as pd
import re
import unicodedata
import html2text
from sqlalchemy import create_engine

chunksize = 1000
user = 'postgres'
password = 'secret'
db_name = 'media_ecosystem'
table_name = 'news_items'

def read_table():
    db_url = 'postgresql://localhost/{}?user={}&password={}'.format(db_name, user, password)
    sql_engine = create_engine(db_url, echo=False)
    conn = sql_engine.connect()

    return pd.read_sql_table(table_name, conn, chunksize=chunksize)  



def get_text_from_html(output_file):
    # HTML2Text keeps formatting, so all paragraphes are saved
    # you get markdown text, so headers are marked with '#' and lists with '*'
    text_maker = html2text.HTML2Text()
    # Do not include any formatting for links
    text_maker.ignore_links = True
    # Do not include any formatting for images
    text_maker.ignore_images = True
    # for using unicode
    text_maker.unicode_snob = True
    text_maker.body_width = 0
    text_maker.single_line_break = True
    # Ignore all emphasis formatting in the html.
    text_maker.ignore_emphasis = True

    table_chunks = read_table()

    df_parts = []

    for chunk in table_chunks:
        chunk['text'] = chunk.text.apply(lambda x: text_maker.handle(x) if pd.notnull(x) else None)
        df_parts.append(chunk)
        del chunk
    df = pd.concat(df_parts)
    df.to_csv(output_file, index=False)


# based on https://github.com/brown-uk/nlp_uk/blob/master/src/main/groovy/org/nlp_uk/other/CleanText.groovy

lat_to_cyr_map = {
    'a': 'а',
    'c': 'с',
    'e': 'е',
    'i': 'і',
    'l': 'І',
    'o': 'о',
    'u': 'и',
    'p': 'р',
    'n': 'п',
    'm': 'т',
    'x': 'х',
    'y': 'у',
    'k': 'к',
    'b': 'ь',
    'r': 'г',
    'A': 'А',
    'B': 'В',
    'C': 'С',
    'E': 'Е',
    'H': 'Н',
    'I': 'І',
    'K': 'К',
    'M': 'М',
    'O': 'О',
    'P': 'Р',
    'T': 'Т',
    'X': 'Х',
    'Y': 'У',
    "á": "а́",
    "Á": "А́",
    "é": "е́",
    "É": "Е́",
    "í": "і́",
    "Í": "І́",
    "ḯ": "ї́",
    "Ḯ": "Ї́",
    "ó": "о́",
    "Ó": "О́",
    "ú": "и́",
    "ý": "у́",
    "Ý": "У́",
    "0": "о"
}

cyr_to_lat_map = {}
for k, v in lat_to_cyr_map.items():
    cyr_to_lat_map[v] = k

APOSTROPHY_LIKE = ('”',
                   '‟',
                   '"',
                   '‘',
                   '′',
                   '\u0313',
                   '΄',
                   '’',
                   '´',
                   '`',
                   '’',
                   '?',
                   '*',
                   )
APOSTROPHY_PREFIX = 'бвгґдзкмнпрстфхш'
APOSTROPHY_SUFFIX = 'єїюя'


def clean(text):
    if pd.notnull(text):
        text = unicodedata.normalize("NFKC", text)
        text = re.sub(r"\\n", "\n", text)
        text = re.sub(r"\n{2,}", "\n", text)
        text = re.sub(r" {2,}", " ", text)
        text = text.strip()

        # change strange apostrophe to '
        text = re.sub(r"([{prefix}])[{apostrophy}]([{suffix}])".format(
            prefix=APOSTROPHY_PREFIX, apostrophy=''.join(APOSTROPHY_LIKE), suffix=APOSTROPHY_SUFFIX),
            r"\1'\2", text, flags=re.IGNORECASE)
        text = re.sub(r"([{prefix}])&#39\s?([{suffix}])".format(
            prefix=APOSTROPHY_PREFIX, suffix=APOSTROPHY_SUFFIX), r"\1'\2", text)

        # add space between sentences if needed (with workaround for  Цензор.НЕТ)
        text = re.sub(r"(?<!Цензор)([\.\?\!])([А-ЯІЇЄҐA-Z])", r"\1 \2", text) 
       
        # clean up latin/cyrillic character mix
        # cases:
        # - latin symbols that look like cyrillic in ukrainian words
        # - cyrillic symbols that look like latin in english words
        text = re.sub(
            r"([бвгґдєжзийклмнптфцчшщьюяБГҐДЄЖЗИЙЛПФХЦЧШЩЬЮЯ]['’ʼ]?)([aceiopxyunmkbr0ABCEHIKMOPTXYáÁéÉíÍḯḮóÓúýÝ])",
            lambda x: x.group(1) + lat_to_cyr_map[x.group(2)], text)

        text = re.sub(
            r"([aceiopxyaceiopxyunmkbr0ABCEHIKMOPTXYáÁéÉíÍḯḮóÓúýÝ])(['’ʼ]?[бвгґдєжзийклмнптфцчшщьюяБГҐДЄЖЗИЙЛПФХЦЧШЩЬЮЯ])",
            lambda x: lat_to_cyr_map[x.group(1)] + x.group(2), text)

        text = re.sub(r"([bdfghjklmnrstuvwzDFGJLNQRSUVWZ]['’ʼ]?)([асеіорхуАВСЕНІКМНОРТХУ])",
                      lambda x: x.group(1) + cyr_to_lat_map[x.group(2)], text)

        text = re.sub(r"([асеіорхуАВСЕНІКМНОРТХУ])(['’ʼ]?[bdfghjklmnrstuvwzDFGJLNQRSUVWZ])",
                      lambda x: cyr_to_lat_map[x.group(1)] + x.group(2), text)

        text = re.sub(r"([а-яіїєґА-ЯІЇЄҐ]['’ʼ]?)([aceiopxyunmkbr0ABCEHIKMHOPTXYáÁéÉíÍḯḮóÓúýÝ])(['’ʼ]?[а-яіїєґА-ЯІЇЄҐ])",
                      lambda x: x.group(1) + lat_to_cyr_map[x.group(2)] + x.group(3), text)

        text = re.sub(r"([a-zA-Z]['’ʼ]?)([асеіорхуАВСЕНІКМНОРТХУ])(['’ʼ]?[a-zA-Z])",
                      lambda x: x.group(1) + cyr_to_lat_map[x.group(2)] + x.group(3), text)

        text = re.sub(r"([а-яіїєґ]\W{0,2} )([ayico])( [А-ЯІЇЄҐа-яіїєґ])",
                      lambda x: x.group(1) + lat_to_cyr_map[x.group(2)] + x.group(3), text)

        text = re.sub(r"([AIYBKOl])( [А-ЯІЇЄҐа-яіїєґ])",
                      lambda x: lat_to_cyr_map[x.group(1)] + x.group(2), text)

    return text


def text_cleaning(df):
    df['text'] = df.text.apply(clean)
    df['title'] = df.title.apply(clean)
    df['subtitle'] = df.subtitle.apply(clean)
    return df

   