# go through virustotal results and find any links to be flagged
import json
import os
import pandas 

def analyze_all():
    # go through each file in the virustotal_results folder
    flagged_links = {}
    for filename in os.listdir('virustotal_results'):
        with open('virustotal_results/' + filename, 'r') as f:
            data = json.load(f)
            engines = data['attributes']['last_analysis_results']
            sus_count = 0
            for engine in engines:
                category = engines[engine]['category']
                result = engines[engine]['result']
                if category == 'malicious' or category == 'phishing' or result == 'malicious' or result == 'phishing':
                    sus_count += 1
            if sus_count > 0:
                flagged_links[filename] = sus_count
                

    with open('flagged.csv', 'w') as f:
        f.write(f'link,flagged_count\n')
        for link in flagged_links:
            f.write(f'{link},{flagged_links[link]}\n')

def analyze_candidates():
    # open candidates links
    candidate_links = []
    data = pandas.read_csv('../../active_html/database/final_candidates.csv')
    for link in data['website']:
        parsed_link = link.split("//")[1]
        if "www." in parsed_link:
            parsed_link = parsed_link.split("www.")[1]
        candidate_links.append(parsed_link)

    # go through and flag candidate sites
    flagged_links = {}
    for filename in os.listdir('virustotal_results'):
        with open('virustotal_results/' + filename, 'r') as f:
            data = json.load(f)
            engines = data['attributes']['last_analysis_results']
            sus_count = 0
            for engine in engines:
                category = engines[engine]['category']
                result = engines[engine]['result']
                if category == 'malicious' or category == 'phishing' or result == 'malicious' or result == 'phishing':
                    sus_count += 1
            candidate_url = ".".join(filename.split('.')[:-1])
            if sus_count > 0 and candidate_url in candidate_links:
                flagged_links[filename] = sus_count

    with open('flaggedCandidates.csv', 'w') as f:
        f.write(f'link,flagged_count\n')
        for link in flagged_links:
            f.write(f'{link},{flagged_links[link]}\n')

def finding_17a():
    # number of candidates with malicious outbound links 
    flagged_links = []
    for filename in os.listdir('virustotal_results'):
        with open('virustotal_results/' + filename, 'r') as f:
            data = json.load(f)
            engines = data['attributes']['last_analysis_results']
            sus_count = 0
            for engine in engines:
                category = engines[engine]['category']
                result = engines[engine]['result']
                if category == 'malicious' or category == 'phishing' or result == 'malicious' or result == 'phishing':
                    sus_count += 1
            if sus_count > 1:
                flagged_links.append(".".join(filename.split('.')[:-1]))
                
    with open('virustotal_mapping.json') as f:
        sus_count = 0
        data = json.load(f)
        for candidate in data:
            for link in data[candidate]:
                if link in flagged_links:
                    print(candidate, link)
                    sus_count += 1
                    break
        print(sus_count)

# analyze_candidates()
# analyze_all()
finding_17a()