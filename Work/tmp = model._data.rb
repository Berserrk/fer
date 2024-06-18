tmp = model._data.cdf_total_assets_agg
tmp[tmp.PARTNER_ID.str.contains("TEST")]

self = model._scenarios.total_assets
df_coown = self.indicators_repo_basic.get_co_owner_partner_ids()

df_ta_struct = self.indicators_repo.total_assets.get_total_assets_structure_field()
df_ta_liquid = self.indicators_repo.total_assets.get_liquid_assets_structured_field()
df_ta_real_estate = self.indicators_repo.total_assets.get_real_estate_assets_structured_field()
df_ta_other = self.indicators_repo.total_assets.get_other_assets_structured_field()

df_ta_free = self.indicators_repo.total_assets.get_free_assets_structured_field()

df_ip_ta = self.indicators_repo.total_assets.get_total_assets_investor_profile()
df_ip_liquid = self.indicators_repo.total_assets.get_liquid_assets_investor_profile()
df_ip_real_estate = self.indicators_repo.total_assets.get_real_estate_assets_investor_profile()
df_ip_other = self.indicators_repo.total_assets.get_other_assets_investor_profile()

df_res = pd.concat(
    [
        df_coown,

        df_ta_struct[df_ta_struct.index.isin(df_coown.index)],
        df_ta_liquid[df_ta_liquid.index.isin(df_coown.index)],
        df_ta_real_estate[df_ta_real_estate.index.isin(df_coown.index)],
        df_ta_other[df_ta_other.index.isin(df_coown.index)],

        df_ta_free[df_ta_free.index.isin(df_coown.index)],

        df_ip_ta[df_ip_ta.index.isin(df_coown.index)],
        df_ip_liquid[df_ip_liquid.index.isin(df_coown.index)],
        df_ip_real_estate[df_ip_real_estate.index.isin(df_coown.index)],
        df_ip_other[df_ip_other.index.isin(df_coown.index)]
    ], axis=1
).rename_axis(index="PARTNER_ID")


def get_filtered_data(indicators, df_coown):
    df_ta_struct = indicators.get_total_assets_structure_field()
    df_ta_liquid = indicators.get_liquid_assets_structured_field()
    df_ta_real_estate = indicators.get_real_estate_assets_structured_field()
    df_ta_other = indicators.get_other_assets_structured_field()
    df_ta_free = indicators.get_free_assets_structured_field()

    df_ip_ta = indicators.get_total_assets_investor_profile()
    df_ip_liquid = indicators.get_liquid_assets_investor_profile()
    df_ip_real_estate = indicators.get_real_estate_assets_investor_profile()
    df_ip_other = indicators.get_other_assets_investor_profile()

    dataframes = [df_ta_struct, df_ta_liquid, df_ta_real_estate, df_ta_other, df_ta_free, df_ip_ta, df_ip_liquid, df_ip_real_estate, df_ip_other]
    dataframes = [df[df.index.isin(df_coown.index)] for df in dataframes]

    return dataframes

def get_asset_data(model):
    tmp = model._data.cdf_total_assets_agg
    tmp = tmp[tmp.PARTNER_ID.str.contains("TEST")]

    total_assets = model._scenarios.total_assets
    df_coown = total_assets.indicators_repo_basic.get_co_owner_partner_ids()

    indicators = total_assets.indicators_repo.total_assets
    dataframes = get_filtered_data(indicators, df_coown)

    df_res = pd.concat([df_coown] + dataframes, axis=1).rename_axis(index="PARTNER_ID")

    return df_res