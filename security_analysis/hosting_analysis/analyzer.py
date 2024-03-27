# look through apivoid results and search for any flagged candidates
import json
import os 

# go throgh apivoid results
flagged_candidates = set()
foreign_host = set()
counter = 0
for candidate in os.listdir("apivoid_results"):
    counter += 1
    data = json.load(open(f"apivoid_results/{candidate}"))
    if data["data"]["report"]["blacklists"]["detections"] > 0:
        flagged_candidates.add(candidate)
    if data["data"]["report"]["server"]["country_code"] != "US":
        foreign_host.add(candidate)

# output
print(f"Total candidates: {counter}")
print(f"Flagged Candidates:")
for candidate in flagged_candidates:
    print(f"{candidate}")
print(f"Foreign Host:")
for candidate in foreign_host:
    print(f"{candidate}")