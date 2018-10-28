
import time
import json
import uuid
import datetime
import sys
import pandas as pd
import copy

from websites import WEBSITES

import os
import errno


DATA_FOLDER = "data/"
if not os.path.exists(os.path.dirname(DATA_FOLDER)):
    os.makedirs(os.path.dirname(DATA_FOLDER))

print "---start---"
start = time.time()

websites_data = {
    "sites": {},
}
for website in WEBSITES:
    website_data = website.scrape_website()
    websites_data["sites"].update(website_data)
    websites_data["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

end = time.time()
print '---end---'
print 'time elapsed: {time_elapsed} seconds'.format(time_elapsed=end-start)

with open("data.json", "w") as outfile:
    json.dump(websites_data, outfile)

csv_json = []
for site_name, flowers in websites_data["sites"].iteritems():
    for flower in flowers:
        new_flower = copy.deepcopy(flower)
        new_flower["site_name"] = site_name
        csv_json.append(new_flower)

df = pd.io.json.json_normalize(
    data=csv_json, 
    # record_path=["site_name"],
    # meta=["site_name", "image", "available", "url", "price"]
)
df.to_csv("data.csv")

