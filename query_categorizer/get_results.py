import requests

HEADERS = {
    'Origin': 'https://www.qwant.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en,fr-FR;q=0.9,fr;q=0.8,en-US;q=0.7,de;q=0.6',
    'Content-type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Referer': 'https://www.qwant.com/',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 '
                  'Safari/537.36 '
}


def get_qwant_result(query, type_="web"):
    params = (
        ('count', '10'),
        ('q', query),
        ('t', type_),
        ('device', 'desktop'),
        ('safesearch', '1'),
        ('locale', 'fr_FR'),
        ('siteLinksExtended', 'true'),
    )

    response = requests.get('https://api.qwant.com/api/search/{}'.format(
        type_), headers=HEADERS, params=params)
    return response.json()["data"]["result"]["items"]
