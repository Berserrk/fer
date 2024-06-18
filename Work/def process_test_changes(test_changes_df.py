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