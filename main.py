
import time
import json
import uuid
import datetime

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

with open("data.json", "w") as outfile:
    json.dump(websites_data, outfile)

end = time.time()
print '---end---'
print 'time elapsed: {time_elapsed} seconds'.format(time_elapsed=end-start)