
import time
import json
import uuid
import datetime

from websites import WEBSITES


if __name__ == "__main__":
    print "---start---"
    start = time.time()

    websites_data = {}
    for website in WEBSITES:
        website_data = website.scrape_website()
        websites_data.update(website_data)

    with open("data/{uuid}--{date}.json".format(uuid=datetime.datetime.now().strftime("%Y-%m-%d"), date=str(uuid.uuid4())[:8]), "w") as outfile:
        json.dump(websites_data, outfile)

    end = time.time()
    print '---end---'
    print 'time elapsed: {time_elapsed} seconds'.format(time_elapsed=end-start)