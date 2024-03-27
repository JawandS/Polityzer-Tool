# go throug candidate mapping and see if any links are flagged
import json

# capture flagged links
flagged_links = set()
with open("flagged.txt", "r") as f:
    for line in f:
        flagged_links.add(line.strip())

# go through candidates
flagged_candidates = set() 
with open("candidate_mapping.json", "r") as f:
    candidate_mapping = json.load(f)
    for candiate in candidate_mapping:
        for link in candidate_mapping[candiate]:
            if link in flagged_links:
                flagged_candidates.add(candiate)
                break

# write flagged candidates
with open("flagged_candidates.txt", "w") as f:
    for candidate in flagged_candidates:
        f.write(candidate + "\n")