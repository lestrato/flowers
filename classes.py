import requests
from bs4 import BeautifulSoup
import json

class Website():
    def __init__(self, domain, name, pages, request, attributes, isAPI = False):
        self.name = name
        self.domain = domain
        self.pages = pages
        self.request = request
        self.data = {}
        self.attributes = attributes
        self.isAPI = isAPI

    def __str__(self):
        return self.name

    def scrape_page(self, page):
        print "> scraping Page %s" % page
        response = page.get_content(self.request, isAPI = self.isAPI)
        if response.status_code != 200:
            print "!! went wrong with the request: code {code}".format(code=response.status_code)
            return False

        attributes_to_get = ["name", "price", "image", "available", "url"]

        all_flower_dom_attributes = {}
        for attribute_name in attributes_to_get:
            attribute = self.attributes.get(attribute_name)
            all_flower_dom_attributes[attribute_name] = page.get_doms_from_path(attribute["path"]) if attribute else []

        page_flowers = {}
        for flower_i  in range(len(all_flower_dom_attributes["name"])):
            flower_name_dom = all_flower_dom_attributes["name"][flower_i]
            flower_name = flower_name_dom
            if self.attributes["name"].get("selector"):
                flower_name = page.get_value_from_dom(flower_name_dom, self.attributes["name"]["selector"])
                if not flower_name:
                    continue
            flower_attributes = {}

            for attribute_name in attributes_to_get:
                flower_attribute_dom = all_flower_dom_attributes[attribute_name]

                if flower_i >= len(flower_attribute_dom):
                    flower_attribute = None
                else:
                    flower_attribute = flower_attribute_dom[flower_i]

                    if attribute_name in self.attributes and "selector" in self.attributes[attribute_name]:
                        flower_attribute = page.get_value_from_dom(flower_attribute_dom[flower_i], self.attributes[attribute_name]["selector"]) if flower_attribute_dom[flower_i] != None else None
                    
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
    def __init__(self, url, attempts = 1):
        self.url = url
        self.content = None
        self.attempts = attempts

    def __str__(self):
        return self.url

    def get_content(self, request, isAPI):
        for retryAttempt in range(0, self.attempts):
            if request["method"] == "POST":
                response = requests.post(self.url, data=request["data"])
            else:
                if isAPI:
                    response = requests.get(self.url, headers={
                        "content-type": "application/json"
                    })

                else:
                    response = requests.get(self.url)

            if response.status_code == 200:
                break

        if response.status_code == 200:
            if isAPI:
                self.content = json.loads(response.text)
            else:
                self.content = BeautifulSoup(response.text, "html.parser")

        return response

    def get_doms_from_path(self, path):
        return path(self.content)

    def get_value_from_dom(self, dom, selector):
        return selector(dom)
