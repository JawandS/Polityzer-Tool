# go through canddiates_to_remove.txt and change those candidates privacy present to false
import json

def remove_candidates():
    with open("candidates_to_remove.txt") as f:
        candidates = []
        for line in f:
            line = line.strip()
            candidates.append(line)
        with open("pruned_privacy_policy_result.json") as data_file:
            data = json.load(data_file)
            for candidate in candidates:
                data[candidate]["privacy_present"] = False
        with open("pruned_privacy_policy_result.json", 'w') as outfile:
            # write to file pretty
            json.dump(data, outfile, indent=1, sort_keys=False)

def get_policy_links():
    # go through all candidates with privacy policies and get the relevant links
    policy_links = {}
    with open("pruned_privacy_policy_result.json") as data_file:
        data = json.load(data_file)
        for candidate in data:
            if data[candidate]["privacy_present"] == True:
                # print privacy_links_with_link_text
                list_of_links = []
                for data_pair in data[candidate]["privacy_links_with_link_text"]:
                    for key in data_pair:
                        list_of_links.append([key, data_pair[key]])
                print("\n\n")
                for idx, link in enumerate(list_of_links):
                    print(idx, link)
                user_choice = input()
                user_choice = int(user_choice) if user_choice.isdigit() else -1
                if user_choice >= 0:
                    policy_links[candidate] = list_of_links[user_choice][1]
        with open("to_download.json", 'w') as outfile:
            # write to file pretty
            json.dump(policy_links, outfile, indent=1, sort_keys=False)

if __name__ == "__main__":
    # remove_candidates()
    get_policy_links()