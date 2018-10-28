from classes import Website, Page

BUDS_TO_GO = Website(
    name = "buds2go",
    domain = "https://www.buds2go.ca",
    pages = [
        Page(
            url="https://www.buds2go.ca/product-category/flowers"
        )
    ],
    request = {
        "method": "POST",
        "data": {
            "alg_products_per_page": -1
        }
    },
    attributes = {
        "name": {
            "path": lambda soup : soup.findAll("", { "class": "product-title" }),
            "selector": lambda dom : dom.text,
        },
        "price": {
            "path": lambda soup : [dom.find("", {"class": "amount"}) for dom in soup.findAll("", { "class": "price-wrapper" })],
            "selector": lambda dom : dom.text,
        },
        "url": {
            "path": lambda soup : [dom.find("a") for dom in soup.findAll("", { "class": "product-title" })],
            "selector": lambda dom : dom["href"],
        },
    },
    # get_detail = {
    #     "available": {
    #         "path": lambda soup : [soup.find("", {"class": "availability"})],
    #         "selector": lambda dom : dom.text,
    #     },
    # }
)

OCS = Website(
    name = "ocs",
    domain = "https://www.ocs.ca",
    pages = [
        Page(
            url="https://ocs.ca/collections/dried-flower-cannabis?page={page_i}".format(page_i=page_i)
        ) for page_i in range(1, 100)
    ],
    request = {
        "method": "GET",
    },
    attributes = {
        "name": {
            "path": lambda soup : soup.findAll("", { "class": "product-tile__title" }),
            "selector": lambda dom : dom.text.strip(),
        },
        "price": {
            "path": lambda soup : soup.findAll("", {"class": "product-tile__price" }),
            "selector": lambda dom : dom.text.strip(),
        },
        "url": {
            "path": lambda soup : [dom.parent for dom in soup.findAll("", { "class": "product-tile__title" })],
            "selector": lambda dom : dom["href"].strip(),
        },
    },
)

REDDIT = Website(
    name = "reddit",
    domain = "https://www.ocs.ca",
    pages = [
        Page(
            url="https://gateway.reddit.com/desktopapi/v1/subreddits/recpics?dist=100&sort=new",
            attempts=20,
        )
    ],
    request = {
        "method": "GET",
    },
    isAPI = True,
    attributes = {
        "name": {
            "path": lambda json: [post["title"].encode('utf-8').strip() for post in json["posts"].values()],
        },
        "image": {
            "path": lambda json: [post["media"]["content"] if post["media"] and post["media"]["type"] == "image" else None for post in json["posts"].values()],
        },
    },
)

WEBSITES = [
    BUDS_TO_GO,
    OCS,
    REDDIT,
]
