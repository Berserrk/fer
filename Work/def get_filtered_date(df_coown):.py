def get_filtered_date(df_coown):
    self = model.scenarios.total_assets
    df_coown = self.indicators_repo.basic.get_co_owner_partner_ids()
    df_ta_struct = self.indicators_repo.total_assets.get_total_assets_structure()

    dataframes = [df_coown, df_ta_struct]
    dataframes = [df[df.index.isin(df_coown.index)] for df in dataframes]
    return  dataframes 