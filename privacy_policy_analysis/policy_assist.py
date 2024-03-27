# comparing the privacy policy manual download vs polityzer 
import pandas as pd 
import os 
import json

# clean dir of json
def clean_dir():
    for office in os.listdir('./polityzer_privacy_policies'):
        for file in os.listdir(f'./polityzer_privacy_policies/{office}'):
            if file.endswith(".json"):
                os.remove(f"./polityzer_privacy_policies/{office}/{file}")

# map the policies from politiyzer to their candidate
def map_policies():
    # open the downlaoded websites csv
    mapping_df = pd.read_csv("../database/downloaded_websites.csv")
    # create a mapping from filepath to candidate name
    mapping = {}
    for index, row in mapping_df.iterrows():
        mapping[row["filepath"].split("/")[3]] = row["name"]
    # go through the files in the directory and replace file names with candidate names
    for office in os.listdir('./polityzer_privacy_policies'):
        for file in os.listdir(f'./polityzer_privacy_policies/{office}'):
            if file in mapping:
                os.rename(f'./polityzer_privacy_policies/{office}/{file}', f'./polityzer_privacy_policies/{office}/{mapping[file]}.html')
            else:
                print(f"no mapping for {office} {file}")

# compare and count files in manual vs polityzer
def analyze_downloads():
    # get all files in polityzer
    polityzer_files = set()
    for office in os.listdir('./privacy_policies'):
        for file in os.listdir(f'./privacy_policies/{office}'):
            polityzer_files.add(file)
    # get files from manual
    manual_files = set()   
    for office in os.listdir('./manual_downloads'):
        for file in os.listdir(f'./manual_downloads/{office}'):
            manual_files.add(file)
    # compare the two sets
    print(f"polityzer: {len(polityzer_files)} manual: {len(manual_files)}")
    print(f"polityzer - manual: {polityzer_files - manual_files}")
    print(f"manual - polityzer: {manual_files - polityzer_files}")

# look at pruned privacy policy result for candidates that should be in downlaods but aren't
def find_missing_candidates():
    # get all files in polityzer
    polityzer_files = set()
    for office in os.listdir('./polityzer_privacy_policies'):
        for file in os.listdir(f'./polityzer_privacy_policies/{office}'):
            polityzer_files.add(file.split(".")[0])
    # read json
    with open("pruned_privacy_policy_result.json") as f:
        all_candidates = json.load(f)
        # create set of candidates that should have policis
        candidates = set()
        for candidate in all_candidates:
            if all_candidates[candidate]["privacy_present"]:
                candidates.add((all_candidates[candidate]["office"], candidate))
        # print difference between sets
        with open('missing_candidates.txt', 'w') as outfile:
            for data in candidates:
                if data[1] not in polityzer_files:
                    outfile.write(f"{data[0]}\n{data[1]}.html\n")

# copy missing candidate data to the privacy policies
def transfer_files():            
    # first line: office, second line: candidate, third linke: file
    with open('missing_candidates.txt', 'r') as f:
        lines = f.readlines()
        for i in range(0, len(lines), 3):
            office = lines[i].strip()
            candidate = lines[i+1].strip()
            file = lines[i+2].strip().replace("\\", "/")
            if file == 'manual':
                # copy from manual downloads
                os.system(f"cp ./manual_downloads/{office}/{candidate} ./privacy_policies/{office}/{candidate}")
            else:
                # copy from html
                os.system(f"cp ../{file} ./privacy_policies/{office}/{candidate}")

# generate a list of all files
def generate_candidate_list():
    base_url = 'https://jawands.github.io/VA-Privacy-Policies/'
    with open('candidate_list.txt', 'w') as f:
        for office in os.listdir('./privacy_policies'):
            for file in os.listdir(f'./privacy_policies/{office}'):
                f.write(f"{base_url}{office}/{file}\n")

# print out the candidates that are missing html
def print_misson_html():
    # read json
    with open("pruned_privacy_policy_result.json") as f:
        all_candidates = json.load(f)
        # create set of candidates that should have policis
        candidates = set()
        for candidate in all_candidates:
            if all_candidates[candidate]["privacy_present"]:
                candidates.add((all_candidates[candidate]["office"], candidate))
        # print difference between sets
        with open('missing_html.txt', 'w') as outfile:
            for data in candidates:
                if not os.path.exists(f"../html/{data[0]}/{data[1]}.html"):
                    outfile.write(f"{data[0]}\n{data[1]}\n")

def find_suggested_text():
    # go through policies and find any with suggested text
    for office in os.listdir('./policy_annotation/policy_text'):
        for file in os.listdir(f'./policy_annotation/policy_text/{office}'):
            with open(f'./policy_annotation/policy_text/{office}/{file}', 'r') as f:
                text = f.read()
                if "suggested" in text:
                    print(f"{office} {file}")

# main method
if __name__ == "__main__":
    # map_policies()
    # clean_dir()
    # find_missing_candidates()
    # transfer_files()
    # analyze_downloads()
    # generate_candidate_list()
    find_suggested_text()