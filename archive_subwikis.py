# archive_subwikis: archive all content pages to the Internet Archive
# now only Timelines wiki

import sys
import time
import requests
from pyquery import PyQuery as pq

ARCHIVE_SAVE_URL = "https://web.archive.org/save/"
DELAY = 2

wikis = {
        'timelines': {
            'base_url': "https://timelines.issarice.com",
            'content_list_query': "/index.php?title=Special%3APrefixIndex&prefix=timeline+of&namespace=0",
            'content_query': ".mw-prefixindex-list a"
            }
        }

links = []

for w in wikis:
    d = pq(url=f"{wikis[w]['base_url']}{wikis[w]['content_list_query']}")
    for link in d(wikis[w]['content_query']).items():
        links.append(wikis[w]['base_url'] + link.attr['href'])

def save_to_internet_archive(url):
    url = f"{ARCHIVE_SAVE_URL}{url}"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.headers['Content-Location']
        result_url = f"https://web.archive.org{result}"
        return result_url
    else:
        print(f"ERROR: {response.status_code}")
        return response

results = []
for l in links:
    results.append(save_to_internet_archive(l))
    time.sleep(DELAY)
print(results)
