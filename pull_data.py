from distutils.command.clean import clean
from re import sub
from textdistance import JaroWinkler
from datetime import date
import csv
import pandas as pd
import math
import string_match_functions as smf
import os

def pull_data():
    outdir = [f'./crosswalks/{date.today()}/', f'./unmatched/{date.today()}/', f'./data/{date.today()}/']
    for item in outdir:
        if not os.path.exists(item):
            os.mkdir(item)

    statesxwalk = pd.DataFrame(pd.read_csv("./data/csvData.csv"))
    statesxwalk = statesxwalk[['State', 'Code']]
    statesxwalk.rename({'State': 'state_longname', 'Code': 'state'}, axis=1, inplace=True)
    mrc11_opeids = pd.DataFrame(pd.read_csv("./data/mrc_table11.csv"))
    mrc10_opeids = pd.DataFrame(pd.read_csv("./data/mrc_table10.csv"))
    mrc1_opeids = pd.DataFrame(pd.read_csv("./data/mrc_table1.csv"))
    mrc11_opeids['institution_name'] = mrc11_opeids['institution_name'].str.lower()
    mrc10_opeids.rename({'czname': 'city'}, axis=1, inplace=True)
    mrc1_opeids.rename({'czname': 'city'}, axis=1, inplace=True)
    mrc10_opeids['name'] = mrc10_opeids['name'].str.lower()
    mrc1_opeids['name'] = mrc1_opeids['name'].str.lower()
    mrc10_opeids['city'] = mrc10_opeids['city'].str.lower()
    mrc1_opeids['city'] = mrc1_opeids['city'].str.lower()
    mrc11_opeids = mrc11_opeids[['super_opeid', 'opeid', 'institution_name', 'superopeid_name']]
    mrc11_opeids.rename({'institution_name': 'name'}, axis=1, inplace=True)
    mrc10_opeids = mrc10_opeids[['super_opeid', 'name', 'state', 'city', 'zip']]
    mrc1_opeids = mrc10_opeids[['super_opeid', 'name', 'state', 'city']]
    full_opeids = pd.concat([mrc10_opeids, mrc1_opeids])
    full_opeids = pd.concat([full_opeids, mrc11_opeids]) # new
    merged_full_opeids = pd.merge(full_opeids, statesxwalk, on='state',how='left')
    merged_full_opeids['name'] = merged_full_opeids['name'].fillna('none')
    merged_full_opeids['name'] = merged_full_opeids['name'].str.strip()
    merged_full_opeids['super_opeid'] = merged_full_opeids['super_opeid'].fillna('none')
    merged_full_opeids['opeid'] = merged_full_opeids['opeid'].fillna('none')
    merged_full_opeids = merged_full_opeids.fillna(int(9999999999))
    merged_full_opeids = merged_full_opeids.replace("", 'none')
    merged_full_opeids['dataset'] = 'chetty-hendren'
    # merged_full_opeids.to_csv(f'./data/{date.today()}/merged_full_opeids.csv')

    print('length of chetty=',len(merged_full_opeids))
    ipeds = pd.DataFrame(pd.read_stata("./data/enrollments_analysis_file_ipeds.dta"))
    ipeds.rename({'instnm': 'name'}, axis=1, inplace=True)
    ipeds['name'] = ipeds['name'].str.lower()
    ipeds['name'] = ipeds['name'].str.strip()
    ipeds['city'] = ipeds['city'].str.lower()
    ipeds = ipeds.replace("", 'none')
    ipeds['name'] = ipeds['name'].fillna('none')
    ipeds['dataset'] = 'ipeds'

    social = pd.DataFrame(pd.read_csv("./data/social_capital_college.csv"))
    social.rename({'college_name': 'name', 'college': 'super_opeid'}, axis=1, inplace=True)
    social['name'] = social['name'].str.lower()
    social['name'] = social['name'].str.strip()
    social['super_opeid'] = social['super_opeid'].astype(str).str[:-2]

    social = social.replace("", 'none')
    social['name'] = social['name'].fillna("none")
    social = social.fillna(int(9999999999))
    social['dataset'] = 'chetty-hendren'
    return merged_full_opeids, social, ipeds


