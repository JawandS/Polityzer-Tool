# go through to_download.json and wget the privacy policies 
import json
import pandas as pd 
import subprocess

# read to download list
to_download_f =  open("to_download.json", "r")
download_list = json.load(to_download_f)
to_download_f.close()

# read the csv file of all candidates
candidates_df = pd.read_csv("../database/candidate_office_website.csv")

TRY_DOWNLOAD = True # flag

# go through candidates in dataframe
for idx in range(len(candidates_df)):
    candidate = candidates_df.loc[idx, "fec_name"]
    office = candidates_df.loc[idx, "office"]
    website = candidates_df.loc[idx, "website"]
    if candidate in download_list:
        policy_link = download_list[candidate]
        if "https" not in policy_link:
            policy_link = website + policy_link
        # wget the privacy policy
        if TRY_DOWNLOAD:
            try:
                subprocess.run(f"wget {policy_link} -O manual_downloads/{office}/{candidate}.html --tries=3", shell=True)
            except Exception as e:
                print(f"Candidate: {candidate} failed to download with error: {e}")

# write the updated download list
# to_download_f =  open("to_download.json", "w")
# json.dump(download_list, to_download_f, indent=1, sort_keys=False)
# to_download_f.close()