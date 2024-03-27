# count how many fields from results are not already in keyword_mapping.json
import json
with open("../active_html/results/form_extractor_result.json") as f:
    data = json.load(f)
    fields = set()
    for candidate in data:
        for field in data[candidate]["form_fields"]:
            fields.add(field)
    with open("data/keyword_mapping.json") as f2:
        mapping = json.load(f2)
        all_fields = set() 
        # add all fields from mapping to set
        for keyword in mapping:
            for field in mapping[keyword]:
                all_fields.add(field)
        for field in fields: # check if field in the mapping
            if field not in all_fields:
                print(field)
        
