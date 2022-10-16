from distutils.command.clean import clean
from re import sub
from textdistance import JaroWinkler, LCSStr
from datetime import date
import csv
import pandas as pd
import math
import string_match_functions as smf
import os
import numpy as np
from pull_data import pull_data


merged_full_opeids, social, ipeds = pull_data()
ipeds = ipeds.drop_duplicates(subset=['unitid'])

outdir = [f'./crosswalks/{date.today()}/', f'./unmatched/{date.today()}/', f'./data/{date.today()}/']
for item in outdir:
    if not os.path.exists(item):
        os.mkdir(item)

all = pd.DataFrame(pd.concat([merged_full_opeids, social], ignore_index=True))
print(all[all.super_opeid == 222178])
all = all.drop_duplicates(subset=['name', 'super_opeid'])

print(len(all.drop_duplicates(subset=['super_opeid', 'name'])))
print(len(ipeds.drop_duplicates(subset=['unitid'])))


crosswalk = pd.DataFrame(pd.read_csv(f'./crosswalks/2022-10-16/chetty_to_ipeds_xwalk_on_subset_2022-10-16.csv'))
print('len of original xwalk=', len(crosswalk))

crosswalk[crosswalk.duplicated(subset=['unitid', 'chetty_hendren_name'], keep=False)].to_csv('dups.csv')

dropped = crosswalk.drop_duplicates(subset=['unitid', 'chetty_hendren_name'])
print('len of xwalk after dropping dups in unitid and name=', len(dropped))



# ipeds_subset = ipeds[~ipeds.unitid.isin(dropped.unitid)]
# chetty_subset = all[~all.super_opeid.isin(dropped.super_opeid)]

# print('len of ipeds_subset=', len(ipeds_subset))
# print('len of chetty_subset=', len(chetty_subset))

# no_matches_chetty = smf.run_all_general(all, ipeds, csv_name=f'./crosswalks/{date.today()}/chetty_to_ipeds_xwalk_on_subset_{date.today()}.csv', name=None)
# no_matches_chetty = pd.DataFrame(no_matches_chetty)
# no_matches_chetty.to_csv(f'./unmatched/{date.today()}/no_matches_chetty_to_ipeds_{date.today()}.csv')

# no_matches_chetty = smf.run_all_general(chetty_subset, ipeds_subset, csv_name=f'./crosswalks/{date.today()}/chetty_to_ipeds_xwalk_refinement_{date.today()}_v7.csv', name=None)
# no_matches_chetty = pd.DataFrame(no_matches_chetty)
# no_matches_chetty.to_csv(f'./unmatched/{date.today()}/refined_no_matches_chetty_to_ipeds_v7.csv')



