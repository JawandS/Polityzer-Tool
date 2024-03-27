# use virus total on the trackers
import json
import os
import time
import tldextract
from virustotal_python import Virustotal
from base64 import urlsafe_b64encode

# get virustotal api key
API_KEY = os.environ.get("VIRUSTOTAL_API_KEY")
DELAY = 30 # seconds
# set up virustotal instance
vtotal = Virustotal(API_KEY=API_KEY, API_VERSION="v3")

# get the links
all_links = set()
with open("flagged.txt", "r") as f:
    for link in f:
        print(link)
        # extract domain
        domain = f"{tldextract.extract(link).domain}.{tldextract.extract(link).suffix}".lower()
        print(domain)
        # add to lists
        all_links.add(domain)

# remove links already downloaded
already_done = set()
for filename in os.listdir("virustotal_results"):
    if filename.endswith(".txt"):
        already_done.add(filename[:-4])
for link in already_done:
    all_links.remove(link)

print(f"Total number of links: {len(all_links)}")

# use virustotal
error_file = open("virustotal_error.log", "a")
for link in all_links:
    print("working on ", link)
    try:
        # sending scan request to virustotal
        response = vtotal.request("urls", data={"url": link}, method="POST")
        url_id = urlsafe_b64encode(link.encode()).decode().strip("=")
        # getting analysis response from virustotal
        analysis_resp = vtotal.request(f"urls/{url_id}")
        response_data = analysis_resp.data
        # write results
        with open(f"virustotal_results/{link}.txt", "w") as f:
            json.dump(response_data, f, indent=2)
        time.sleep(DELAY)
    except Exception as err:
        print(f"An error occurred: {err}\nCatching and continuing with program.")
        error_file.write(link + "\t" + str(err) + "\n")
        if "429" in str(err):
            print("quota exceeded")
            break
        time.sleep(DELAY)