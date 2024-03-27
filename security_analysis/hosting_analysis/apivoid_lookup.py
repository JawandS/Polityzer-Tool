import os
import csv
import requests
import json
from urllib.parse import urlparse, urljoin
import time
import tldextract
import pandas as pd

# open APIVoid
API_KEY = os.environ.get("APIVOID_KEY")
API_ENDPOINT = (
    f"https://endpoint.apivoid.com/domainbl/v1/pay-as-you-go/?key={API_KEY}&host="
)

# get the websites
websites = {}
site_df = pd.read_csv("../https_analysis/active_sites_1_7.csv")
for index, row in site_df.iterrows():
    websites[row["fec_name"]] = row["website"]

print(f"websites: {len(websites)}")

for cand_name in websites:
    cand_website = websites[cand_name]
    print("working on", cand_name, cand_website)
    output_file = f"apivoid_results/{cand_name}.json"
    if os.path.isfile(output_file):
        continue
    with open(output_file, "w") as f:
        cand_website = (
            tldextract.extract(cand_website).domain
            + "."
            + tldextract.extract(cand_website).suffix
        )
        request_url = API_ENDPOINT + cand_website
        print(request_url)
        # break
        request = requests.get(request_url)
        response = request.json()
        json.dump(response, f, indent=2)
        time.sleep(1)