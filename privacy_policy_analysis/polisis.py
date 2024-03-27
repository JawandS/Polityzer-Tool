import json
import time
import requests
import os

API_KEY=os.environ.get("POLISIS_API_KEY")
# BASE_DIR=os.path.dirname(os.getcwd())
headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Mobile Safari/537.36"
}
# POLICY_DIR = "/Users/kaushal/git/website/jekyll/kaflekaushal.github.io/assets/policy/remaining/validated"
# output_dir = "/Users/kaushal/git/website/jekyll/kaflekaushal.github.io/assets/policy/remaining/validated/output"
output_dir = "./polisis_output"

if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

url = "https://pribot.org/api/web/analyzeNewPolicy"
error_file = open(os.path.join(output_dir, "errors.tsv"), "w")

# payload = {"url": policy_url + policyfile, "key": f"{API_KEY}"}
# response = requests.request("POST", url=url, headers=headers, json=payload)
# print(response.json())
# print(response)


# get urls from candidate_list.txt
url_list = []
with open("candidate_list.txt") as f:
    for line in f:
        url_list.append(line.strip())

count = 0
for policy_url in url_list:
    candidate_name = policy_url.split("/")[-1].split(".")[0]
    # if not policyfile.startswith("president_inactive"):
    #     continue
    
    print("working on", candidate_name)
    # candidate_file = "|".join(policyfile.split("|")[1:])[:-4] + "json"

    payload = {"url": policy_url, "key": f"{API_KEY}"}
    response = requests.request("POST", url=url, headers=headers, json=payload)
    print(response)
    try:
        response_json = response.json()
        output_file = f"{candidate_name}.json"

        with open(output_file, "w") as f:
            json.dump(response_json, f, indent=2)
    except Exception as e:
        print("ERROR", str(e))
        error_file.write(candidate_name + "\t" + str(response) + "\t" + str(e) + "\n")
    exit()
    for i in range(61):
        print("waiting", i + 3, "sec")
        time.sleep(1)

# sample_policy_html=open(os.path.join(POLICY_DIR,current_dirname,current_filename)).read()
