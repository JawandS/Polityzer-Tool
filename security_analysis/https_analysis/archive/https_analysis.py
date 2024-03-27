import pandas as pd

# read the csv
candidate_df = pd.read_csv('candidate_htpps_test_12_12.csv')
# drop rows that have error or 429
candidate_df = candidate_df[(candidate_df['https_result'] != 'Error') and (candidate_df['https_result'] != '429') and (candidate_df['http_result'] != 'Error') and (candidate_df['http_result'] != '429')]
# print out unique codes from https_result column
print(f"Unique https_result codes: {candidate_df['https_result'].unique()}")
# print out unique codes from http_result column
print(f"Unique http_result codes: {candidate_df['http_result'].unique()}")
# write that have differnet https_result and http_result codes
flagged_candidate_df = pd.DataFrame()
# iteratre through candiate df
for index, row in candidate_df.iterrows():
    # get data
    candidate_name = row['fec_name']
    office = row['office']
    website = row['website']
    https_result = row['https_result']
    http_result = row['http_result']
    # if https_result and http_result are different
    if https_result != http_result:
        # add to flagged df
        flagged_candidate_df = pd.concat([flagged_candidate_df, pd.DataFrame({'fec_name': candidate_name, 'office': office, 'website': website, 'https_result': https_result, 'http_result': http_result}, index=[0])])
# save flagged df
flagged_candidate_df.to_csv('./flagged_candidate_htpps_test_12_12.csv', index=False)