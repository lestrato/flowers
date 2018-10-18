import requests
from bs4 import BeautifulSoup

class Website():
    def __init__(self, domain, name, pages, request, attributes):
        self.name = name
        self.domain = domain
        self.pages = pages
        self.request = request
        self.data = {}
        self.attributes = attributes

    def __str__(self):
        return self.name

    def scrape_page(self, page):
        print "> scraping Page %s" % page
        response = page.get_content(self.request)
        if response.status_code != 200:
            print "!! went wrong with the request: code {code}".format(code=response.status_code)
            return False

        attributes_to_get = ["name", "price", "available", "url"]

        all_flower_dom_attributes = {}
        for attribute_name in attributes_to_get:
            attribute = self.attributes.get(attribute_name)
            all_flower_dom_attributes[attribute_name] = page.get_doms_from_path(attribute["path"]) if attribute else []

        page_flowers = {}
        for flower_i  in range(len(all_flower_dom_attributes["name"])):
            flower_name_dom = all_flower_dom_attributes["name"][flower_i]
            flower_name = page.get_value_from_dom(flower_name_dom, self.attributes["name"]["selector"])
            flower_attributes = {}

            for attribute_name in attributes_to_get:
                flower_attribute_dom = all_flower_dom_attributes[attribute_name]
                flower_attribute = page.get_value_from_dom(flower_attribute_dom[flower_i], self.attributes[attribute_name]["selector"]) if flower_i < len(flower_attribute_dom) and flower_attribute_dom[flower_i] != None else None
                if flower_attribute and attribute_name == "url":
                    if flower_attribute.startswith("/"):
                        flower_attribute = '{domain}{url}'.format(domain=self.domain, url=flower_attribute)
                    elif flower_attribute.startswith("http"):
                        pass
                    else:
                        flower_attribute = '{domain}/{url}'.format(domain=self.domain, url=flower_attribute)

                flower_attributes[attribute_name] = flower_attribute
            
            page_flowers[flower_name] = flower_attributes

        if page_flowers == {} :
            print "!! there were no flowers found, exiting site"
            return False

        return page_flowers

    def scrape_website(self):
        print "> scraping Website %s" % self.name
        website_data = {
          "site": {},
          "flowers": {},
        }
        for page in self.pages:
            page_flowers = self.scrape_page(page)
            if page_flowers == False:
                break
            website_data["flowers"].update(page_flowers)
        website_data["site"]["domain"] = self.domain

        return { self.name: website_data }

class Page():
    def __init__(self, url):
        self.url = url
        self.soup = None

    def __str__(self):
        return self.url

    def get_content(self, request):
        if request["method"] == "POST":
            response = requests.post(self.url, data=request["data"])
        else:
            response = requests.get(self.url)

        if response.status_code == 200:
            self.soup = BeautifulSoup(response.text, "html.parser")
        
        return response

    def get_doms_from_path(self, path):
        return path(self.soup)

    def get_value_from_dom(self, dom, selector):
        return selector(dom)
