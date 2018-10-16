import requests
import datetime
from bs4 import BeautifulSoup
import json
import uuid

class Website():
    def __init__(self, name, pages, request, paths):
        self.name = name
        self.pages = pages
        self.request = request
        self.data = {}
        self.paths = paths

    def __str__(self):
        return self.name

    def scrape_page(self, page):
        print '> scraping Page %s' % page
        page.get_content(self.request)

        flower_names = page.get_doms_from_path(self.paths['name'])
        flower_prices = page.get_doms_from_path(self.paths['price'])

        for (flower_name, flower_price) in zip(flower_names, flower_prices):
            yield { flower_name.text: flower_price.text }

    def scrape_website(self):
        print '> scraping Website %s' % website
        website_data = {}
        for page in self.pages:
            for data in self.scrape_page(page):
                website_data.update(data)

        return { self.name: website_data }

class Page():
    def __init__(self, url):
        self.url = url
        self.soup = None

    def __str__(self):
        return self.url

    def get_content(self, request):
        if request['method'] == "POST":
            response = requests.post(self.url, data=request['data'])
        else:
            response = requests.get(self.url)

        self.soup = BeautifulSoup(response.text, "html.parser")

    def get_doms_from_path(self, path):
        return path(self.soup)

BUDS_TO_GO = Website(
    name = 'buds2go',
    pages = [
        Page(
            url='https://www.buds2go.ca/product-category/flowers'
        )
    ],
    request = {
        'method': 'POST',
        'data': {
            'alg_products_per_page': -1
        }
    },
    paths = {
        'name': lambda soup : soup.findAll("", { 'class': 'product-title' }),
        'price': lambda soup : [dom.find("", {'class': 'amount'}) for dom in soup.findAll("", { 'class': 'price-wrapper' })],
    }
)

WEBSITES = [
    BUDS_TO_GO,
]


if __name__ == '__main__':
    print '---start---'
    websites_data = []
    for website in WEBSITES:
        website_data = website.scrape_website()
        websites_data.append(website_data)
    print websites_data
    with open('data/{uuid}--{date}.json'.format(uuid=datetime.datetime.now().strftime("%Y-%m-%d"), date=str(uuid.uuid4())[:8]), 'w') as outfile:
        json.dump(websites_data, outfile)