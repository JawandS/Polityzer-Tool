# go through the candidates list and see if responds to an http vs https get request

import pandas as pd
import requests
# read candidate csv
candiate_df = pd.read_csv('../database/candidate_office_website.csv')
result_df = pd.DataFrame(columns=['fec_name', 'office', 'website', 'https_result', 'http_result'])
# go through candidate list
for index, row in candiate_df.iterrows():
    # get data
    candidate_name = row['fec_name']
    office = row['office']
    website = row['website']
    # print
    print(f"testing https candidate {candidate_name}; {index} of {len(candiate_df)}")
    # perform a get request on the website
    try:
        https_result = str(requests.get(website).status_code)
    except:
        https_result = "Error"
for index, row in candiate_df.iterrows():
    # get data
    candidate_name = row['fec_name']
    office = row['office']
    website = row['website']
    # print
    print(f"testing http candidate {candidate_name}; {index} of {len(candiate_df)}")
    # perform a get request on the website
    try:
        http_result = str(requests.get(website.replace('https', 'http')).status_code)
    except:
        http_result = "Error"
    # add to result dataframe
    print(f"{candidate_name} https result: {https_result} http result: {http_result}")
    result_df = pd.concat([result_df, pd.DataFrame({'fec_name': candidate_name, 'office': office, 'website': website, 'https_result': https_result, 'http_result': http_result}, index=[0])])
# save result dataframe
result_df.to_csv('./candidate_htpps_test_12_12.csv', index=False)