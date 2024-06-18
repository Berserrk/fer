def generate_id(prefix, id, length):
    return prefix + str(id).zfill(length)

def process_actions(current_dataframe, action, current_synthetic_id, current_legacy_id, current_test_synthetic_id, current_test_legacy_id):
    field_id_to_replace = action['field_id_to_replace']
    current_dataframe_id = getattr(current_dataframe, field_id_to_replace, None)
    if current_dataframe_id is None:
        return
    if action['partner_id_to_use'] == 'synth': 
        filter_condition = current_dataframe_id.isin([current_synthetic_id])
        replacement_id = current_test_synthetic_id
    else: 
        filter_condition = current_dataframe_id.isin([current_legacy_id])
        replacement_id = current_test_legacy_id
    record_to_copy = current_dataframe.loc[filter_condition].copy()
    record_to_copy[field_id_to_replace] = replacement_id
    action['to_append'].append(record_to_copy)

def process_filters(cur_df_id, cur_df_pk_list, id, key_value_list):
    cur_filter = cur_df_id.isin([id])
    for index, pk_column in enumerate(cur_df_pk_list):
        cur_cond = cur_df_pk_list[index].isin([key_value_list[index]])
        cur_filter = cur_filter & cur_cond
    return cur_filter

def process_test_data(test_data_df, synth_legacy_partner_dict, raw_repo_test_meta_dict, raw_repo, test_partner_ids):
    for test_partner in test_data_df.itertuples():
        current_synthetic_id = test_partner.synthPartnerID
        current_legacy_id = synth_legacy_partner_dict.get(current_synthetic_id)
        current_test_synthetic_id = generate_id('TESTID', test_partner.testID, 10)
        current_test_legacy_id = generate_id('TESTLEG', test_partner.testID, 9)
        test_partner_ids.append(current_test_synthetic_id)

        for method, actions in raw_repo_test_meta_dict.items():
            current_dataframe = getattr(raw_repo, method, None)
            if current_dataframe is None:
                continue
            for action in actions['actions']:
                process_actions(current_dataframe, action, current_synthetic_id, current_legacy_id, current_test_synthetic_id, current_test_legacy_id)

    update_append_raw_repo_dfs()

def process_test_changes(test_changes_df_merged, synth_legacy_partner_dict, raw_repo_test_meta_dict, raw_repo):
    for test_change in test_changes_df_merged.itertuples():
        cur_synth_id = test_change.synthPartnerID
        cur_legacy_id = synth_legacy_partner_dict.get(cur_synth_id)
        cur_test_synth_id = generate_id('TEST_ID', test_change.testID, 10)
        cur_test_legacy_id = generate_id('TESTLEG', test_change.testID, 9)

        cur_df = getattr(raw_repo, test_changes['dataframe'])
        cur_field_to_replace = test_change.columnName
        cur_field_id = raw_repo_test_meta_dict[test_change['dataframe']]['id']
        cur_df_id = getattr(cur_df, cur_field_id)
        cur_field_pk_list = raw_repo_test_meta_dict[test_change['dataframe']]['pk']
        cur_df_pk_list = [getattr(cur_df, pk) for pk in cur_field_pk_list]
        key_value_list = test_change.keyValue.split(',')
        
        if raw_repo_test_meta_dict[test_change['dataframe']]['type'] == 'synth':
            cur_filter = process_filters(cur_df_id, cur_df_pk_list, cur_test_synth_id, key_value_list)
        else:
            cur_filter = process_filters(cur_df_id, cur_df_pk_list, cur_test_legacy_id, key_value_list)
        
        cur_df.loc[cur_filter, cur_field_to_replace] = test_change['value']
        raw_repo_test_meta_dict[test_change['dataframe']]['new_df'] = cur_df

test_changes_df_merged = pd.merge(test_changes_df, test_data_df, on='testID', how='inner')
process_test_changes(test_changes_df_merged, synth_legacy_partner_dict, raw_repo_test_meta_dict, raw_repo)