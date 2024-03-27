import json
import os

def finding_7a():
    # look at candidates without a privacy disclosure but collect PII
    # open the mapping into a dictionary
    with open('../form_analysis/data/keyword_mapping.json') as f:
        mapping = json.load(f)
        reverse_mapping = {}
        # reverse the mapping to go from label to keyword
        for keyword in mapping:
            # get the list of labels for the keyword
            labels = mapping[keyword]
            # add each label to the reverse mapping
            for label in labels:
                reverse_mapping[label] = keyword
    # go through the form data
    candidates_with_data = []
    with open('../active_html/results/form_extractor_result.json') as f:
        data = json.load(f)
        for candidate in data:
            collects_pii = False
            for field in data[candidate]["form_fields"]:
                field = field.lower().replace('\n', '').replace('\t', '').replace('*', '').strip()
                if reverse_mapping[field] not in ["ignore"]:
                    collects_pii = True
            if collects_pii:
                candidates_with_data.append(candidate)
    print(f"candidates with data: {len(candidates_with_data)}")
    # compare to the privacy policy data
    candidates_without_privacy = []
    with open('../active_html/results/privacy_policy_result.json') as f:
        privacy_policy_data = json.load(f)
        for candidate in candidates_with_data:
            if privacy_policy_data[candidate]["privacy_present"] == False:
                candidates_without_privacy.append(candidate)
    # output results
    print("Candidates without a privacy policy but collect PII:")
    print(len(candidates_without_privacy))

def finding_10a():
    # look through all privacy policies for hte keywork retain or retention
    for candidate in os.listdir('policy_annotation/policy_text/House'):
        with open(f'policy_annotation/policy_text/House/{candidate}', 'r', encoding="utf8") as f:
            policy = f.read()
            if "retain" in policy or "retention" in policy.lower():
                print(candidate)
    for candidate in os.listdir('policy_annotation/policy_text/Senate'):
        with open(f'policy_annotation/policy_text/Senate/{candidate}', 'r', encoding="utf8") as f:
            policy = f.read()
            if "retain" in policy or "retention" in policy.lower():
                print(candidate)

def finding_13a():
    # look through all privacy policies for hte keywork retain or retention
    for candidate in os.listdir('policy_annotation/policy_text/House'):
        with open(f'policy_annotation/policy_text/House/{candidate}', 'r', encoding="utf8") as f:
            policy = f.read()
            if "winred" in policy.lower():
                print(candidate)
    for candidate in os.listdir('policy_annotation/policy_text/Senate'):
        with open(f'policy_annotation/policy_text/Senate/{candidate}', 'r', encoding="utf8") as f:
            policy = f.read()
            if "winred" in policy.lower():
                print(candidate)

# finding_7a()
# finding_10a()
finding_13a()