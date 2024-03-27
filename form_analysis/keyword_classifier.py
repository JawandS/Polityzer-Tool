# go through the form fields from results and map to using the ontology in keyword_mapping.json
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
    
    # keep track of the number of times each keywork appears
    keyword_count = {}

    # go through form extractor in results 
    with open('../results/form_extractor_result.json') as f2:
        candidate_data = json.load(f2)
        # go through each candidate and increment the keywork counts
        for candidate in candidate_data:
            candidate_office = candidate_data[candidate]['office']
            keywords = set()
            for field in candidate_data[candidate]['form_fields']:
                keywords.add(reverse_mapping[field])
            for keyword in keywords:
                if keyword in keyword_count:
                    # 0: house, 1: senate
                    if candidate_office == 'House':
                        keyword_count[keyword][0] += 1
                    else:
                        keyword_count[keyword][1] += 1
                else:
                    # 0: house, 1: senate
                    if candidate_office == 'House':
                        keyword_count[keyword] = [1, 0]
                    else:
                        keyword_count[keyword] = [0, 1]

# write the keyword counts sorted by highest to lowest to file
with open('data/keyword_count.csv', 'w') as f:
    house_candidates = 79
    senate_candidates = 42
    f.write('keyword, house_count, house_percent, senate_count, senate_percent\n')
    for keyword in sorted(keyword_count, key=lambda k: keyword_count[k][0] + keyword_count[k][1], reverse=True):
        house_count = keyword_count[keyword][0]
        senate_count = keyword_count[keyword][1]
        f.write(keyword + ', ' + str(house_count) + ', ' + str(round(house_count / house_candidates * 100, 2)) + ', ' + str(senate_count) + ', ' + str(round(senate_count / senate_candidates * 100, 2)) + '\n')