dataframes_list = {
    'df_advisor': {'partnerID': synth_partner_ids},
    'df_busra': {'partnerID': synth_partner_ids},
    'df_contact': {'PARTNER_ID': synth_partner_ids}
}

for df_name, filters in dataframes_list.items():
    for column, values in filters.items():
        df = getattr(raw_repo, df_name)
        df_filter = filter_dataframe_by_ids(df, values, column)
        setattr(raw_repo, df_name, filtered_df)

def update_raw_repos_dfs():
    for key in raw_repo_test_meta_dict.keys():
        setattr(raw_repo, key, raw_repo_test_meta_dict[key]['new_df'])

def update_append_raw_repos_dfs():
    for method in dir(raw_repo):
        if not method in raw_repo_test_meta_dict.keys():
            continue
        cur_df = getattr(raw_repo, method)
        if raw_repo_test_meta_dict[method]['df_type'] == 'koalas':
            cur_to_append =  ks.concat(raw_repo_test_meta_dict[method]['to_append'])
            cur_df = ks.concat([cur_df, cur_to_append], ignore_index=True)
        else:
            cur_to_append = pd.concat(raw_repo_test_meta_dict[method]['to_append'])
            cur_df = pd.concat([cur_df, cur_to_append], ignore_index=True)
        raw_repo_test_meta_dict[method]['new_df'] = cur_df
    
test_partner_ids = []

def process_test_data(test_data_df, synth_legacy_partner_dict, raw_repo_test_meta_dict, raw_repo, test_partner_ids):
    for index, test_partner in test_data_df.iterrows():
        current_synthetic_id = test_partner['synthPartnerID']
        current_legacy_id = synth_legacy_partner_dict.get(current_synthetic_id)
        current_test_synthetic_id = 'TESTID' + str(test_partner['testID'].zfill(10))
        current_test_legacy_id = 'TESTLEG' + str(test_partner['testID'].zfill(9))
        test_partner_ids.append(current_test_synthetic_id)

        for method, actions in raw_repo_test_meta_dict.items():
            current_dataframe = getattr(raw_repo, method, None)
            if current_dataframe is None:
                continue
            for action in actions['actions']:
                field_id_to_replace = action['field_id_to_replace']
                current_dataframe_id = getattr(current_dataframe, field_id_to_replace, None)
                if current_dataframe_id is None:
                    continue
                if action['partner_id_to_use'] == 'synth': 
                    filter_condition = current_dataframe_id.isin([current_synthetic_id])
                    replacement_id = current_test_synthetic_id
                else: 
                    filter_condition = current_dataframe_id.isin([current_legacy_id])
                    replacement_id = current_test_legacy_id
                record_to_copy = current_dataframe.loc[filter_condition].copy()
                record_to_copy[field_id_to_replace] = replacement_id
                actions['to_append'].append(record_to_copy)

    update_append_raw_repo_dfs()


def process_test_changes(test_changes_df_merged, synth_legacy_partner_dict, raw_repo_test_meta_dict, raw_repo):
    for index, test_change in test_changes_df_merged.iterrows():
        cur_synth_id = test_change['synthPartnerID']
        cur_legacy_id = synth_legacy_partner_dict.get(cur_synth_id)
        cur_test_synth_id= 'TEST_ID' + str(test_change['testID']).zfill(10)
        cur_test_legacy_id= 'TESTLEG' + str(test_change['testID']).zfill(9)

        cur_df = getattr(raw_repo, test_change['dataframe'])
        cur_field_to_replace = test_change['columnName']
        cur_field_id = raw_repo_test_meta_dict[test_change['dataframe']]['id']
        cur_df_id = getattr(cur_df, cur_field_id)
        cur_field_pk_list = raw_repo_test_meta_dict[test_change['dataframe']]['pk']
        cur_df_pk_list = [getattr(cur_df, pk) for pk in cur_field_pk_list]
        key_value_list = test_change['keyValue'].split(',')
        
        if raw_repo_test_meta_dict[test_change['dataframe']]['type'] == 'synth':
            cur_filter = cur_df_id.isin([cur_test_synth_id])
            for index, pk_column in enumerate(cur_df_pk_list):
                cur_cond = cur_df_pk_list[index].isin([key_value_list[index]])
                cur_filter = cur_filter & cur_cond
            cur_df.loc[cur_filter, cur_field_to_replace] = test_change['value']
        else:
            cur_filter = cur_df_id.isin([cur_test_legacy_id])
            for index, pk_column in enumerate(cur_df_pk_list):
                cur_cond = cur_df_pk_list[index].isin([key_value_list[index]])
                cur_filter = cur_filter & cur_cond
            cur_df.loc[cur_filter, cur_field_to_replace] = test_change['value']
        raw_repo_test_meta_dict[test_change['dataframe']]['new_df']= cur_df


test_changes_df_merged = pd.merge(test_changes_df, test_data_df, on='testID', how='inner')
process_test_changes(test_changes_df_merged, synth_legacy_partner_dict, raw_repo_test_meta_dict, raw_repo)