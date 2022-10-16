from re import sub

def threshold_check_general(dict, similarity, r, m, chetty, matched_by=None, thresh=0.90):
    '''
    Function for checking similarity threshold checks
    Input:
        dict (dictionary): Holds potential matches
        similarity (int): JaroWinkler similarity score
        r, m (tuple): single college records in the form of a tuple.
    Output:
        dict (dictionary): list of matches.
    '''
    if similarity > thresh: 
        if 'opeid' in chetty.columns:
            ### Adds all records to linked dict if a match
            # dict[(m.unitid, m.name, m.dataset)] = (r.super_opeid, r.opeid, r.name, similarity, r.dataset, matched_by, thresh) #changed
            dict[(r.super_opeid, r.name, r.dataset)] = (m.unitid, m.name, similarity, m.dataset, matched_by, thresh) #changed
        else:
            ### Adds all records to linked dict if a match
            # dict[(m.unitid, m.name, m.dataset)] = (r.super_opeid, 'none', r.name, similarity, r.dataset, matched_by, thresh)
            dict[(r.super_opeid, r.name, r.dataset)] = (m.unitid, m.name, similarity, m.dataset, matched_by, thresh)
    return dict

def make_subsets(r, ipeds):
    subs = ipeds

    if r.name not in ['9999999999', 'none', '', ' ']:
        subs = ipeds[ipeds.name.str.contains(r.name[0:3], na=False, case=True)]
    return subs

def check_zips(z1, z2):
    '''Return true or false'''

    if (z1 not in ['9999999999', 'none', '', ' ']) & (z2 not in ['9999999999', 'none', '', ' ']):
        return True
    else:
        return False

def check_state(z1, z2):
    '''Return true or false'''

    if (z1 not in ['9999999999', 'none', '', ' ']) & (z2 not in ['9999999999', 'none', '', ' ']):
        return True
    else:
        return False

def find_matches_general_chetty_to_ipeds(chetty, ipeds, name=None, main_links=[]):
    # To edit further for Prof Dan Black/Pro Sloane
    """
    Find_matches is a nested loop where the outer loop runs through all dirty restaurants in ri_restaurants table
    and finds matches to every other restaurant besides itself in the table. Once its compiled a list of linked lists, 
    it runs that list-of-lists through the function remove_duplicates, to remove duplicates matches.
    Input: 
        None
    Output:
        list-of-list of linked lists. 
    """
    from textdistance import JaroWinkler, LCSStr

    jar = JaroWinkler()
    no_match = []


    for r in chetty.itertuples(index=True):
        # block on starting letters to reduce run time
        dict = {}
        if isinstance(r.name, (str)):
            highest_name = 0
            highest_tot_sim = 0

            subs = make_subsets(r, ipeds)
            
            for m in subs.itertuples(index=True):
                ipe = list(map(str, [m.name, m.statefip, m.city, m.zip]))
                ope = list(map(str, [r.name, int(r.zip)]))

                name = jar.similarity(ope[0], ipe[0])
                if name > 0.97:
                    if (name > highest_name): # 
                        highest_name = name
                        # if check_zips(ipe[3], ope[1]):
                        #     matched_by='name_zip'
                        #     zipcode = jar.similarity(ipe[3], ope[1])
                        #     if zipcode > 0.8999:
                        #         tot_sim = (0.70 * name) + (0.30 * zipcode)
                        #         if tot_sim > highest_tot_sim:
                        #             highest_tot_sim = tot_sim
                        #             dict = threshold_check_general(dict, tot_sim, r, m, chetty, thresh=0.9, matched_by=matched_by)
                        #             print(tot_sim)
                        #     else:
                        #         continue
                        # else:
                        matched_by='name_only'
                        dict = threshold_check_general(dict, name, r, m, chetty, thresh=0.90, matched_by=matched_by)
        print(dict)
        if len(dict) > 0:
            main_links.append(dict)
        else:
            no_match.append(r)

    return main_links, no_match

def run_all_general(df1, df2, csv_name, name=None):
    import csv

    already_written = []

    with open(csv_name,'w') as f:
        headers = ['super_opeid', 'unitid', 'chetty_hendren_name', 'ipeds_name', 
        'similarity', 'dataset_2', 'dataset_1',  'matched_using', 'acceptance_threshold']
        
        writer = csv.writer(f)
        writer.writerow(headers)
        # main_dict, no_match = find_matches_general(df1, df2, name=name)
        main_dict, no_match = find_matches_general_chetty_to_ipeds(df1, df2, name=name)
        for d in main_dict:
            for key, val in d.items():
                ids1, name1, dataset1 = key
                ids2, name2, similarity, dataset2, matched, thresh = val
                
                row = [ids1, ids2, name1, name2, similarity, dataset1, dataset2, matched, thresh]

                if (ids1, ids2) in already_written:
                    continue
                else:
                    already_written.append((ids1, ids2))
                    writer.writerow(row)
    return no_match

