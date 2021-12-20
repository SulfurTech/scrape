import csv

import requests
from bs4 import BeautifulSoup


HEADERS = ({'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Accept-Language': 'en,en-US',
            'Referrer Policy': 'strict-origin-when-cross-origin',
            'SameSite': None})

# URL = "https://stepik.org/catalog"
# URL = "https://stepik.org/catalog/72" # trending python
# URL = "https://stepik.org/catalog/73" # trending java
# URL = "https://stepik.org/catalog/71" # trending kotlin
URL = "https://stepik.org/catalog/68" # computer science

# discovery-card-link bg-white text-black
r = requests.get(URL, headers=HEADERS)
# with open("stepik.html", 'wb') as f:
#     f.write(r.content)

soup = BeautifulSoup(r.text, 'html.parser')
# print(soup.find_all('li', 'course-cards__item'))
courses = []
for course in soup.find_all('li', 'course-cards__item'):
    title = course.find('a', class_='course-card__title')
    authors = course.find('a', class_='course-card__author')
    price = course.find('span', class_='format-price')
    image = course.find('img', class_='course-card__cover')
    rating = course.find('span', class_='course-card__widget', attrs={"data-type":"rating"})
    if title is None or authors is None or price is None:
        continue

    link = URL + title.get('href')
    image = "https://stepik.org" + image.get('src')
    title = title.string.strip()
    authors = authors.string.strip()
    price = price.text if "Free" not in price.text else "0"
    rating = rating.text.strip() if rating is not None else 0

    course = {
        "title": title,
        "authors": authors,
        "price": float(price.replace("$","")),
        "link": link,
        "image": image,
        "rating": float(rating)
    }
    courses.append(course)
    print(course)

filename = 'stepik_courses.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f, ['image', 'link', 'authors', 'title', 'price', 'rating'])
    w.writeheader()
    aaa = map(lambda row: w.writerow(row), courses)
    list(aaa)
    for course in courses:
        w.writerow(course)
# quotes = [] # a list to store quotes
#
# tab = soup.find_all("li", {'class': 'ais-InfiniteHits-item'})
# div.tab-contents > div > div > div > div > ul > li:nth-child(1) > div > div > a > div > div.cds-69.card-info.css-0.cds-71.cds-grid-item
# temp = tab.findAll(lambda tag: tag.name == 'h2')
# for row in tab.findAll('h2', class_='card-title'):
#     quote = {}
#     # quote['theme'] = row.h5.text
#     # quote['url'] = row.a['href']
#     # quote['img'] = row.img['src']
#     # quote['lines'] = row.img['alt'].split(" #")[0]
#     # quote['author'] = row.img['alt'].split(" #")[1]
#     quote['name'] = row.h2.text
#     print(row)
#     quotes.append(quote)
#

