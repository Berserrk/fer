


def convert_to_datetime(df, column, format):
    """
    Convert a DataFrame column to datetime format.

    Parameters:
    df (pandas.DataFrame): The DataFrame to convert.
    column (str): The column in df to convert.
    format (str): The datetime format string to use for conversion.

    Returns:
    pandas.DataFrame: The DataFrame with the converted column.
    """
    df[column] = df[column].astype(str)
    df[column] = pd.to_datetime(df[column], format=format)
    return df 

def filter_by_date(df, date_column, start_column, end_column):
    """
    Filter a DataFrame by a date range.

    Parameters:
    df (pandas.DataFrame): The DataFrame to filter.
    date_column (str): The column in df with the dates to filter by.
    start_column (str): The column in df with the start of the date range.
    end_column (str): The column in df with the end of the date range.

    Returns:
    pandas.DataFrame: The filtered DataFrame.
    """
    filter_df =  df[date_column].between(df[start_column], df[end_column])
    return df.loc[filter_df]

def filter_by_partner_ids(df, column, ids):
    """
    Filter a DataFrame by partner IDs.

    Parameters:
    df (pandas.DataFrame): The DataFrame to filter.
    column (str): The column in df with the partner IDs.
    ids (list): The partner IDs to filter by.

    Returns:
    pandas.DataFrame: The filtered DataFrame.
    """
    filter_df = df[column].isin(ids)
    return df.loc[filter_df]

def create_partner_dict(df, partner_column, legacy_column):
    """
    Create a dictionary mapping partner IDs to legacy IDs.

    Parameters:
    df (pandas.DataFrame): The DataFrame with the partner and legacy IDs.
    partner_column (str): The column in df with the partner IDs.
    legacy_column (str): The column in df with the legacy IDs.

    Returns:
    dict: A dictionary mapping partner IDs to legacy IDs.
    """
    partner_dict ={}
    for index, item in df.iterrows():
        partner_dict[item[partner_column]] = item[legacy_column]
    return partner_dict

def filter_dataframe_by_ids(df, ids, column_name):
    """
    Filter a DataFrame by a list of IDs.

    Parameters:
    df (pandas.DataFrame): The DataFrame to filter.
    ids (list): The IDs to filter by.
    column_name (str): The column in df with the IDs.

    Returns:
    pandas.DataFrame: The filtered DataFrame.
    """
    filter_df = df[column_name].isin(ids)
    return df.loc[filter_df]

def update_raw_repos_dfs():
    """
    Update the DataFrames in raw_repo with new DataFrames from raw_repo_test_meta_dict.

    This function assumes that raw_repo_test_meta_dict is a dictionary where the keys are
    the names of DataFrames in raw_repo, and the values are dictionaries with a 'new_df'
    key, where the value is the new DataFrame to replace the old one with.
    """
    for key in raw_repo_test_meta_dict.keys():
        setattr(raw_repo, key, raw_repo_test_meta_dict[key]['new_df'])

def update_append_raw_repos_dfs():
    """
    Append new DataFrames to the existing DataFrames in raw_repo.

    This function assumes that raw_repo_test_meta_dict is a dictionary where the keys are
    the names of DataFrames in raw_repo, and the values are dictionaries with a 'to_append'
    key, where the value is a list of DataFrames to append to the existing DataFrame.
    """
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