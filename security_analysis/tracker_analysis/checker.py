# go through outbound links for candidates and flag potential trackers
import re 
import json
import time
from adblockparser import AdblockRules

# open files
flagged_links = open("flagged.txt", "a+")
clean_links = open("clean.txt", "a+")

# read data from easyprivacy.txt
raw_rules = []
with open("easyprivacy.txt", "r") as f:
    for line in f:
        if line.startswith('!') or line.startswith('@@'): # comment
            continue
        else:
            raw_rules.append(line.strip())
rules = AdblockRules(raw_rules)

# gather all outbound and site links
all_candidates = set()
with open('../../active_html/results/link_extractor_result.json', 'r') as f:
    data = json.load(f)
    # go through links
    for candidate in data:
        # add website
        all_candidates.add(candidate)

# read from files into sets
analyzed_links = set()
for line in flagged_links:
    analyzed_links.add(line.strip())
for line in clean_links:
    analyzed_links.add(line.strip())

# get outbound links
outbound_links = set()
candidate_mapping  = {candidate: [] for candidate in all_candidates}
for candidate in all_candidates:
    # get candidate data
    for link in data[candidate]['outbound_links']:
        if link not in analyzed_links:
            outbound_links.add(link)
        candidate_mapping[candidate].append(link)
with open("candidate_mapping.json", "w") as f:
    json.dump(candidate_mapping, f, indent=2)
del candidate_mapping
del analyzed_links

print(f"Total number of links: {len(outbound_links)}")
print(f"Total number of rules: {len(raw_rules)}")

# go through outbound links and check if they are trackers
start_time = time.time()
counter = 0
for link in outbound_links:
    if rules.should_block(link):
        flagged_links.write(link + "\n")
        print(f"flagged: {link}")
    else:
        clean_links.write(link + "\n")
    counter += 1
    if counter % 100 == 0:
        print(f"{counter} / {len(outbound_links)} links analyzed")
    
# write to file
flagged_links.close()
clean_links.close()