def convert_to_datetime(df, column, format):
    df[column] = df[column].astype(str)
    df[column] = pd.to_datetime(df[column], format=format)
    return df 

def filter_by_date(df, date_column, start_column, end_column):
    filter_df =  df[date_column].between(df[start_column], df[end_column])
    return df.loc[filter_df]

def filter_by_partner_ids(df, column, ids):
    filter_df = df[column].isin(partner_ids)
    return df.loc[filter_df]

def create_partner_dict(df, partner_column, legacy_column):
    partner_dict ={}
    for index, item in df.iterrows():
        partner_dict[item[partner_column]] = item[legacy_column]
    return partner_dict

def filter_dataframe_by_ids(df, ids, column_name):
    filter_df = df[column_name].isin(ids)
    return df.loc[filter_df]

test_data_df = convert_to_datetime(test_data_df, 'validFrom', '%Y-%m-%d')
test_data_df = convert_to_datetime(test_data_df, 'validTo', '%Y-%m-%d')
test_data_df['now'] = datetime.today().strftime('%Y-%m-%d')
test_data_df = convert_to_datetime(test_data_df, 'now', '%Y-%m-%d')

synth_test_partner_ids = filter_by_partner_ids(raw_repo.df_key_dir, 'partnerId', synth_test_partner_ids)
legacy_partner_ids = set(df_key_dir_filtered['legacyPartnerId'].tolist())
synth_legacy_partner_df = df_key_dir_filtered.filter(items=['partnerId', 'legacyPartnerId']).drop_duplicates()

synth_legacy_partner_dict = create_partner_dict(synth_legacy_partner_df, 'partnerId', 'legacyPartnerId')

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
    
test_patner_ids = []

