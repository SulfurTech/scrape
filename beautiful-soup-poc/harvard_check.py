import requests
from bs4 import BeautifulSoup


HEADERS = ({'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Accept-Language': 'en,en-US',
            # 'Referrer Policy': 'strict-origin-when-cross-origin',
            })
URL = "https://pll.harvard.edu/catalog"
r = requests.get(URL, headers=HEADERS)
with open("harvard.html", 'wb') as f:
    f.write(r.content)

soup = BeautifulSoup(r.text, 'html.parser')