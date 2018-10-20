
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

websites_data = {}
for website in WEBSITES:
    website_data = website.scrape_website()
    websites_data.update(website_data)

with open("{data_folder}/{uuid}--{date}.json".format(data_folder=DATA_FOLDER, uuid=datetime.datetime.now().strftime("%Y-%m-%d"), date=str(uuid.uuid4())[:8]), "w") as outfile:
    json.dump(websites_data, outfile)

end = time.time()
print '---end---'
print 'time elapsed: {time_elapsed} seconds'.format(time_elapsed=end-start)