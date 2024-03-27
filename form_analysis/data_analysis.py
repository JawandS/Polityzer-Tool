# count the number of house and senate candidates that have at least one form field not in ignore
import json

# open the mapping into a dictionary
with open('data/keyword_mapping.json') as f:
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
with open("../active_html/results/form_extractor_result.json") as f:
    data = json.load(f)
    for candidate in data:
        house = False
        senate = False
        clean_fields = []
        for field in data[candidate]["form_fields"]:
            field = field.lower().replace('\n', '').replace('\t', '').replace('*', '').strip()
            if reverse_mapping[field] not in ["ignore"]:
                clean_fields.append(reverse_mapping[field])
        if "political_opinions" in clean_fields:
            print(candidate)
            print(clean_fields)
        