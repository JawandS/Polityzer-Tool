# python file to help map for fields to keywords
import json

# open the results file
with open("./form_extractor_result.json") as f:
    data = json.load(f)
    # go through an get all of the form fields
    form_fields = set()
    for candidate in data:
        for field in data[candidate]["form_fields"]:
            form_fields.add(field)
    # go through the form fields and map to keywords
    keyword_mapping = {
        "name": [],
        "email": [],
        "phone_number": [],
        "location_coarse": [],
        "location_fine": [],
        "non-pii": [],
        "misc": [],
        "ignore": []
    }
    mapping = {
        "0": "name",
        "1": "email",
        "2": "phone_number",
        "3": "location_coarse",
        "4": "location_fine",
        " ": "misc",
        "": "ignore"
    }
    print(f"{len(form_fields)} form fields found")
    for field in form_fields:
        keyword = input(f"{field}: ")
        if keyword not in mapping:
            keyword = "6"
        keyword_mapping[mapping[keyword]].append(field)
    # output result to file
    with open("keyword_mapping.json", "w") as f:
        json.dump(keyword_mapping, f, indent=4)
    with open("keyword_mapping.txt", "w") as f:
        for keyword in keyword_mapping:
            f.write(f"{keyword}: {keyword_mapping[keyword]}\n")
    