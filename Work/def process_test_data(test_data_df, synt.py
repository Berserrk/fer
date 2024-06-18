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


test_changes_df_merged = pd.merge(test_changes_df, test_data_df, on='testID', how='inner')


for index, test_change in test_changes_df_merged.iterrows():
    cur_synth_id = test_change['synthPartnerID']
    cur_legacy_id = synth_legacy_partner_dict.get(cur_synth_id)
    cur_test_synth_id= 'TEST_ID' + str(test_change['testID']).zfill(10)
    cur_test_legacy_id= 'TESTLEG' + str(test_change['testID']).zfill(9)

    cur_df = getattr(raw_repo, test_changes['dataframe'])
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
