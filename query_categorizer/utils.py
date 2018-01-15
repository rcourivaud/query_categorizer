import re


def clean_results(results):
    return [
        {k: clean_text(clean_html(v)) for k, v in res.items() if k in ['desc', 'title', 'url']} for res in results
    ]


def clean_html(raw_html):
    clean_regex = re.compile('<.*?>')
    return re.sub(clean_regex, '', raw_html)


def clean_text(text,
               filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
               lower=True):
    if lower:
        text = text.lower()

    translate_map = str.maketrans(filters, " " * len(filters))

    text = text.translate(translate_map)
    return re.sub(' +', ' ', text)
