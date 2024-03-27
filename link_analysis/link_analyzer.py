# look at the inbound/outbound links for candidates
import json

# load data
data = json.load(open('../active_html/results/link_extractor_result.json'))

def find_common_links():
    # go through outbound links and see the most common domains
    outbound_links = {}
    for candidate in data:
        candidate_link_set = set()
        for link in data[candidate]['outbound_links']:
            domain = link.split('/')[2]
            candidate_link_set.add(domain)
        for domain_name in candidate_link_set:
            if domain_name not in outbound_links:
                outbound_links[domain_name] = 1
            else:
                outbound_links[domain_name] += 1

    # print the top 10 domains
    print('Top 10 outbound domains:')
    for domain in sorted(outbound_links, key=outbound_links.get, reverse=True)[:10]:
        print(domain, outbound_links[domain])

    # log all the outbound links to file sorted by the link count
    with open('link_counts.txt', 'w') as outfile:
        for domain in sorted(outbound_links, key=outbound_links.get, reverse=True):
            outfile.write(domain + ' ' + str(outbound_links[domain]) + '\n')

def finding_12a_13():
    # find candidates that either use platform1 or platform2
    platform_one = "winred"
    platform_two = "actblue"
    candidates_using_platform = []
    platform_one_users = []
    for candidate in data:
        all_links = data[candidate]['outbound_links']
        for link in all_links:
            if platform_one in link:
                platform_one_users.append(candidate)
            if platform_one in link or platform_two in link:
                candidates_using_platform.append((candidate, data[candidate]['office']))
                break
    print('Candidates using platform1 or platform2:', len(candidates_using_platform))
    print(f'Senate candidates: {len([x for x in candidates_using_platform if x[1] == "Senate"])}')
    print(f'House candidates: {len([x for x in candidates_using_platform if x[1] == "House"])}')

    # check if these candidates have a privacy disclosure
    privacy_data = json.load(open('../privacy_policy_analysis/pruned_privacy_policy_result.json'))
    p1_candidates = []
    missing_policy = 0
    for candidate in candidates_using_platform:
        candidate = candidate[0]
        if privacy_data[candidate]['privacy_present'] == False:
            missing_policy += 1
        elif candidate in platform_one_users:
            p1_candidates.append(candidate)
    print('Candidates missing privacy policy:', missing_policy)
    for candidate in p1_candidates:
        print(candidate)

finding_12a_13()