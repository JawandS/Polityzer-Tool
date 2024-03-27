import os
import pandas as pd

# get the list of html files in the directory
candidates_with_html = []
for file in os.listdir("active_html/Senate"):
    candidates_with_html.append(file)
for file in os.listdir("active_html/House"):
    candidates_with_html.append(file)

print(f"{len(candidates_with_html)} html files found")
print(candidates_with_html[:5])

# get the list of candidate names from candidates.csv
candidates_df = pd.read_csv("database/all_candidate_office_website.csv")
candidates = candidates_df["fec_name"].tolist()

# output the list of candidate names that don't have html files
to_write = ""
no_html_counter = 0
for candidate in candidates:
    if candidate not in candidates_with_html:
        to_write += f"{candidates_df.loc[candidates_df['fec_name'] == candidate].values[0]}\n"
        no_html_counter += 1
    else: # check for empty html
        office = "Senate" if candidate in (os.listdir("active_html/Senate")) else "House"
        candidate_path = f"active_html/{office}/{candidate}"
        html_files = [f for f in os.listdir(candidate_path) if os.path.isfile(os.path.join(candidate_path, f))] 
        if len(html_files) == 1:
            print(f"Possible Emtpy File: {candidate}")
            if os.stat(f"active_html/{office}/{candidate}/{html_files[0]}").st_size == 0:
                to_write += f"{candidates_df.loc[candidates_df['fec_name'] == candidate].values[0]}\n"
                no_html_counter += 1
# with open("missing_html_list.txt", "w") as f:
#     f.write(f"{no_html_counter} / {len(candidates)} missing html file\n")
#     f.write(to_write)