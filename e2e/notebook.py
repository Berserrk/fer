def test_end2end_pipeline():
    spark = util_functions.spark_builder(technical_config.log_verbosity, is_test=True)
    data_load_task = DataLoadTask(technical_config.args, is_test=True)

    raw_repo = AuthoritativeDataRepo()
    raw_repo.load_data(data_load_task)


    df_shopping_list_pich = data_load_task.read(load_task.skr_shopping_list_input())
    df_pich_dates = df_shopping_list_pich.filter(df_shopping_list_pich.processingDate == '12022024')

    if len(df_pich_dates.head(1)) == 0:
        df_distinct_processingdate = df_shopping_list_pich.select("processingDate").distinct()
        processingDate_list = list(distinct_processingDate.select("processingDate").toPandas()['processingDate'])

    # Removing those not included in df_partner_br to avoid model crash with old shopping lists
    from pyspark.sql.functions import col

    original_shopping_list = list(df_pich_dates.select("PARTNER_ID").drop_duplicates().toPandas().PARTNER_ID)
    df_pich = df_pich_dates.join(
        raw_repo.df_partner_br.to_spark().withColumn("PARTNER_ID", col("PARTNER_ID")).select('PARTNER_ID').drop_duplicates(), on="PARTNER_ID").toPandas()

    not_anymore_clients = [x for x in original_shopping_list if x not in (df_pich.PARTNER_ID.unique())]

    # Remove PARTNER_ID if in not_anymore_clients
    not_anymore_clients = [x for x in not_anymore_clients if x != "PARTNER_ID"]

    raw_repo.df_pich = df_pich

    # START NOTEBOOK CODE
    # Read the Test Cases Input File
    import os
    import pandas as pd
    test_data_df = pd.read_csv(file_path_input_test_cases_end2end_pipeline + "/skr_test_input.csv")
    test_changes_file = pd.read_csv(file_path_input_test_cases_end2end_pipeline + "/skr_test_changes.csv")
    test_output_file = pd.read_csv(file_path_input_test_cases_end2end_pipeline + "/skr_test_output.csv")

    test_data_df = pd.read_csv(path_to_test_input_file)
    test_changes_df = pd.read_csv(path_to_test_changes_file)
    test_output_df = pd.read_csv(path_to_test_output_file)
    
    test_data_df['validFrom'] = test_data_df['validFrom'].astype(str)
    test_data_df['validTo'] = test_data_df['validTo'].astype(str)

    test_data_df['validFrom'] = pd.to_datetime(test_data_df['validFrom'], format="%Y%m%d")
    test_data_df['validTo'] = pd.to_datetime(test_data_df['validTo'], format="%Y%m%d")
    test_data_df['now'] = pd.to_datetime(test_data_df['now'], format="%Y%m%d")
    test_data_df['now'] = pd.to_datetime(test_data_df['now'], format="%Y%m%d")

    filter_test_data_df = test_data_df.now.between(test_data_df['validFrom'], test_data_df['validTo'])
    test_data_df = test_data_df.loc[filter_test_data_df]

    # We obtain the synth partner ids in scope as well as their legacy ids
    synth_partner_ids = set(test_data_df['synthPartnerID'])

    filter_df_key_dir = raw_repo.df_key_dir.partnerID.isin(synth_partner_ids)
    df_key_dir_filtered = raw_repo.df_key_dir.loc[filter_df_key_dir]
    legacy_partner_ids = set(df_key_dir_filtered['legacyPartnerID'].tolist())
    synth_legacy_partner_df = df_key_dir_filtered.filter(items=['partnerID', 'legacyPartnerID']).drop_duplicates()

    synth_legacy_partner_dict = {}
    for index, synth_legacy_item in synth_legacy_partner_df.iterrows():
        synth_legacy_partner_dict[synth_legacy_item['partnerID']] = synth_legacy_item['legacyPartnerID']

    # Filter and transform the input meq dp Data
    filter_df_advisor = raw_repo.df_advisor.partnerID.isin(synth_partner_ids)
    filter_df_busra = raw_repo.df_busra.partnerID.isin(synth_partner_ids)
    filter_df_contact_contact = raw_repo.df_contact.contact.partnerID.isin(legacy_partner_ids)
    filter_df_contract = raw_repo.df_contract.partnerID.isin(synth_partner_ids)
    filter_df_investor_profile = raw_repo.df_investor_profile.partnerID.isin(synth_partner_ids)

    filter_df_key_dir = raw_repo.df_key_dir.partnerID.isin(synth_partner_ids)
    filter_df_longt = raw_repo.df_longt.partnerID.isin(synth_partner_ids)
    filter_df_other_pr = raw_repo.df_other_pr.partnerID.isin(synth_partner_ids)
    filter_df_pa_pa_rel = raw_repo.df_pa_pa_rel.partnerID.isin(synth_partner_ids)
    filter_df_pa_pa_pro = raw_repo.df_pa_pa_pro.partnerID.isin(synth_partner_ids)
    filter_df_partner_br = raw_repo.df_partner_br.partnerID.isin(synth_partner_ids)
    filter_df_partner_rel = raw_repo.df_partner_rel.partnerID.isin(synth_partner_ids)
    filter_df_pich = raw_repo.df_pich.PARTNER_ID.isin(synth_partner_ids)
    filter_df_position_cash = raw_repo.df_position_cash.partnerID.isin(legacy_partner_ids)
    filter_df_position_loan = raw_repo.df_position_loan.partnerID.isin(legacy_partner_ids)
    filter_df_position_securities = raw_repo.df_position_securities.partnerID.isin(legacy_partner_ids)
    filter_df_purpose = raw_repo.df_purpose.partnerID.isin(synth_partner_ids)
    filter_df_sensitive = raw_repo.df_sensitive.partnerID.isin(synth_partner_ids)
    filter_df_sensitive_smt = raw_repo.df_sensitive_smt.partnerID.isin(synth_partner_ids)
    filter_df_tac = raw_repo.df_tac.partnerID.isin(synth_partner_ids)
    filter_df_trx = raw_repo.df_trx.partnerID.isin(legacy_partner_ids)
    filter_df_trx_comments = raw_repo.df_trx_comments.partnerID.isin(synth_partner_ids)

    raw_repo.df_advisor = raw_repo.df_advisor.loc[filter_df_advisor]
    raw_repo.df_busra = raw_repo.df_busra.loc[filter_df_busra]
    raw_repo.df_contact_contact = raw_repo.df_contact_contact.loc[filter_df_contact_contact]
    raw_repo.df_contract = raw_repo.df_contract.loc[filter_df_contract]
    raw_repo.df_investor_profile = raw_repo.df_investor_profile.loc[filter_df_investor_profile]
    raw_repo.df_key_dir = raw_repo.df_key_dir.loc[filter_df_key_dir]
    raw_repo.df_longt = raw_repo.df_longt.loc[filter_df_longt]
    raw_repo.df_other_pr = raw_repo.df_other_pr.loc[filter_df_other_pr]
    raw_repo.df_pa_pa_rel = raw_repo.df_pa_pa_rel.loc[filter_df_pa_pa_rel]
    raw_repo.df_pa_pa_pro = raw_repo.df_pa_pa_pro.loc[filter_df_pa_pa_pro]
    raw_repo.df_partner_br = raw_repo.df_partner_br.loc[filter_df_partner_br]
    raw_repo.df_partner_rel = raw_repo.df_partner_rel.loc[filter_df_partner_rel]
    raw_repo.df_pich = raw_repo.df_pich.loc[filter_df_pich]
    raw_repo.df_position_cash = raw_repo.df_position_cash.loc[filter_df_position_cash]
    raw_repo.df_position_loan = raw_repo.df_position_loan.loc[filter_df_position_loan]
    raw_repo.df_position_securities = raw_repo.df_position_securities.loc[filter_df_position_securities]
    raw_repo.df_purpose = raw_repo.df_purpose.loc[filter_df_purpose]
    raw_repo.df_sensitive = raw_repo.df_sensitive.loc[filter_df_sensitive]
    raw_repo.df_sensitive_smt = raw_repo.df_sensitive_smt.loc[filter_df_sensitive_smt]
    raw_repo.df_tac = raw_repo.df_tac.loc[filter_df_tac]
    raw_repo. df_trx = raw_repo.df_trx.loc[filter_df_trx]
    raw_repo.df_trx_comments = raw_repo.df_trx_comments.loc[filter_df_trx_comments]

def update_raw_repo_dfs():
    raw_repo.df_advisor = raw_repo_test_meta_dict['df_advisor']['new_df']
    raw_repo.df_busra = raw_repo_test_meta_dict['df_busra']['new_df']
    raw_repo.df_contact_contact = raw_repo_test_meta_dict['df_contact_contact']['new_df']
    raw_repo.df_contract = raw_repo_test_meta_dict['df_contract']['new_df']
    raw_repo.df_investor_profile = raw_repo_test_meta_dict['df_investor_profile']['new_df']
    raw_repo.df_key_dir = raw_repo_test_meta_dict['df_key_dir']['new_df']
    raw_repo.df_longt = raw_repo_test_meta_dict['df_longt']['new_df']
    raw_repo.df_other_pr = raw_repo_test_meta_dict['df_other_pr']['new_df']
    raw_repo.df_pa_pa_rel = raw_repo_test_meta_dict['df_pa_pa_rel']['new_df']
    raw_repo.df_pa_pa_pro = raw_repo_test_meta_dict['df_pa_pa_pro']['new_df']
    raw_repo.df_partner_br = raw_repo_test_meta_dict['df_partner_br']['new_df']
    raw_repo.df_partner_rel = raw_repo_test_meta_dict['df_partner_rel']['new_df']
    raw_repo.df_pich = raw_repo_test_meta_dict['df_pich']['new_df']
    raw_repo.df_position_cash = raw_repo_test_meta_dict['df_position_cash']['new_df']
    raw_repo.df_position_loan = raw_repo_test_meta_dict['df_position_loan']['new_df']
    raw_repo.df_position_securities = raw_repo_test_meta_dict['df_position_securities']['new_df']
    raw_repo.df_sensitive = raw_repo_test_meta_dict['df_sensitive']['new_df']
    raw_repo.df_sensitive_smt = raw_repo_test_meta_dict['df_sensitive_smt']['new_df']
    raw_repo.df_tac = raw_repo_test_meta_dict['df_tac']['new_df']
    raw_repo.df_purpose = raw_repo_test_meta_dict['df_purpose']['new_df']
    raw_repo.df_trx = raw_repo_test_meta_dict['df_trx']['new_df']
    raw_repo.df_trx_comments = raw_repo_test_meta_dict['df_trx_comments']['new_df']

def update_append_raw_repo_dfs():
    for methode in dir(raw_repo):
        if not method in raw_repo_test_meta_dict.keys():
            continue
        cur_df = getattr(raw_repo, method)
        if raw_repo_test_meta_dict[method]['df_type'] =='koalas':
            cur_to_append = ks.concat(raw_repo_test_meta_dict[method]['to_append'])
            cur_df = ks.concat([cur_df, cur_to_append], ignore_index=True)
        else:
            cur_to_append = pd.concat(raw_repo_test_meta_dict[method]['to_append'])
            cur_df = pd.concat([cur_df, cur_to_append], ignore_index=True)
        raw_repo_test_meta_dict[method]['new_df'] = cur_df
    update_raw_repo_dfs()

test_partner_ids = []

for index, test_partner in test_data_df.iterrows():
    cur_synth_id = test_partner['synthPartnerID']
    cur_legacy_id = synth_legacy_partner_dict[cur_synth_id]
    cur_test_synth_id = 'TEST_ID' + str(test_partner['testID']).zfill(10)
    cur_test_legacy_id = 'TEST_LEG' + str(test_partner['testID']).zfill(9)
    test_partner_ids.append(cur_test_synth_id)

    for method in dir(raw_repo):
        if not method in raw_repo_test_meta_dict.keys():
            continue
        cur_df = getattr(raw_repo, method)
        for action in raw_repo_test_meta_dict[method]['actions']:
            cur_field_id_to_replace = action['field_id_to_replace']
            cur_df_id = getattr(cur_df, cur_field_id_to_replace)
            if action['partner_id_to_use'] == 'synth':
                cur_filter = cur_df_id.isin([cur_synth_id])
                cur_record_to_copy = cur_df.loc[cur_filter].copy()
                cur_record_to_copy[cur_field_id_to_replace] = cur_test_synth_id
            else:
                cur_filter = cur_df_id.isin([cur_legacy_id])
                cur_record_to_copy = cur_df.loc[cur_filter].copy()
                cur_record_to_copy[cur_field_id_to_replace] = cur_test_legacy_id
            raw_repo_test_meta_dict[method]['to_append'].append(cur_record_to_copy)
    
    update_append_raw_repo_dfs
    test_changes_df_merged = pd.merge(test_changes_df, test_data_df, on='testID', how='inner')

    for index, test_change in test_changes_df_merged.iterrows():
        cur_synth_id = test_change['synthPartnerID']
        cur_legacy_id = synth_legacy_partner_dict[cur_synth_id]
        cur_test_synth_id = 'TEST_ID' + str(test_change['testID']).zfill(10)
        cur_test_legacy_id = 'TEST_LEG' + str(test_change['testID']).zfill(9)

        cur_df = getattr(raw_repo, test_change['dataframe'])
        cur_field_id_to_replace = test_change['columnName']
        cur_field_id = raw_repo_test_meta_dict[test_change['dataframe']]['id']
        cur_df_id = getattr(cur_df, cur_field_id)
        cur_field_pk_list = raw_repo_test_meta_dict[test_change['dataframe']]['pk']
        cur_df_pk_list = [getattr(cur_df, x) for x in cur_field_pk_list]
        key_value_list = test_change['keyValue'].split(',')
        if raw_repo_test_meta_dict[test_change['dataframe']]['df_type'] == 'synth':
            cur_filter = cur_df_id.isin([cur_test_synth_id])
            for index, pk_column in enumerate(cur_field_pk_list):
                cur_cond = cur_df_pk_list[index].isin([key_value_list[index]])
                cur_filter = cur_filter & cur_cond
            cur_df.loc[cur_filter, cur_field_id_to_replace] = test_change['value']
        else:
            cur_filter = (cur_df_id.isin([cur_test_legacy_id]))
            for index, pk_column in enumerate(cur_field_pk_list):
                cur_cond = cur_df_pk_list[index].isin([key_value_list[index]])
                cur_filter = cur_filter & cur_cond
            cur_df.loc[cur_filter, cur_field_id_to_replace] = test_change['value']
        raw_repo_test_meta_dict[test_change['dataframe']]['new_df'] = cur_df

    update_raw_repo_dfs()

shopping_list = pd.Series(list(raw_repo.df_pich.PARTNER_ID.unique()), name='PARTNER_ID')
print("shopping_list_value_counts:", shopping_list.value_counts())
raw_repo.load_shopping_list_info(date=technical_config.exec_config.CALCULATION_DATE,
                                 partner_ids=shopping_list)

partner_ids_in_scope, partner_ids_out_of_scope = \
    shopping_list_processing.apply_include_exclude_rules(raw_repo.df_shopping_list_info)

"""Final scope division"""

partner_ids_in_scope = partner_ids_in_scope.drop_duplicates()
partner_ids_out_of_scope = partner_ids_out_of_scope.drop_duplicates()

partner_ids_in_scope = partner_ids_in_scope[~partner_ids_in_scope.isin(partner_ids_out_of_scope)]

scope_ids = list(partner_ids_in_scope) + list(partner_ids_out_of_scope)
legal_entities_and_old_clients = []
for id in shopping_list:
    if id not in scope_ids:
        legal_entities_and_old_clients.append(id)
for id in not_anymore_clients:
    legal_entities_and_old_clients.append(id)
tmp = pd.Series(legal_entities_and_old_clients)
partner_ids_out_of_scope = pd.concat([partner_ids_out_of_scope, tmp])

print(f"IN SCOPE POPULATION: {len(partner_ids_in_scope)}")
print(f"IN SCOPE POP list", partner_ids_in_scope)
print(f"OUT OF SCOPE POPULATION: {len(partner_ids_out_of_scope)}")

###
### Run the pipeline with the filtered and modified data Part 2
"""Map Data"""

AuthoritativeDataMapper.use_koalas()
print("all_partner_ids", raw_repo.all_partner_ids.count())
print("df_busra", raw_repo.df_busra.count())
print("df_advisor", raw_repo.df_advisor.count())
print("df_contract", raw_repo.df_contract.count())
data_repo = AuthoritativeDataMapper.map_data(raw_repo,
                                             technical_config.exec_config,
                                             partner_ids_in_scope,
                                             partner_ids_out_of_scope)
# kprint("data repo count", data_repo.count())
data_repo.partner_scope = {"IN": partner_ids_in_scope, "OUT": partner_ids_out_of_scope}
print("data_repo partner_scope count", data_repo.partner_scope)
data_repo.prepare_data()

"""Final run of the model"""

model = Review(technical_config.exec_config)
model._data = data_repo
print("model data", model._data)
model._indicators = IndicatorRepo(model._data)
print("model_indicators:", model._indicators)
model._scenarios = ScenariosRepo(model._data
                                 
"""DQ Checks"""
model._checks = DataChecker(data_repo)
model._checks.complete_check()
"""Final model evaluation"""
model.evaluate_modules()
"""Writing Model Output to msgbp Start"""
# set shopping list date received from the arguments in dmy format
modelShoppingListTimestamp_dmy = "12022024"
df_model_output_pd = model.interface.file.copy()
print("df_model_output_pd steps", df_model_output_pd.count())
print("df_model_output_pd steps\n", df_model_output_pd)
df_model_output_pd['SHOPPING_LIST_DATE'] = modelShoppingListTimestamp_dmy
print("df_model_output_pd shopping_list_date", df_model_output_pd['SHOPPING_LIST_DATE'])
# Convert Panda df to Spark dataframe for power write
df_model_output = spark.createDataFrame(df_model_output_pd.astype(str))
print("df_model_output", df_model_output.count())
print("df_model_outputs", df_model_output.show())

output_data_df = pd.read_csv(path_to_test_output_file)
output_input_merged_df = pd.merge(test_data_df, output_data_df, on="testID", how='inner')
print("output_input_merged_df", len(output_input_merged_df))
print("output_input_merged_df sum flag true", output_input_merged_df['flag'].sum())
import pyspark.sql.functions as F
test_partner_ids_list = [F.lit(x) for x in test_partner_ids]
model_output_keep_cols = [
    'PARTNER_STID', 'FINDING_CODE', 'FINDING_STATUS_CD'
]
df_model_output_filtered = (
    df_model_output
    .select(model_output_keep_cols)
    .filter(
        F.col('PARTNER_STID').isin(test_partner_ids_list)
        # keep only testpartners
    )
)
print("test_partner_ids_list",test_partner_ids_list)
print("df_model_output_filtered",df_model_output_filtered.count())
print("df_model_output_filtered groupby partner_stid count =",df_model_output_filtered.groupby(('PARTNER_STID')).count().show())
#create pyspark sparkSession
spark = SparkSession.builder \
    .getOrCreate()
#create PySpark DataFrame from Pandas
output_input_merged_df_spark=spark.createDataFrame(output_input_merged_df)
output_input_merged_df_spark = (
    output_input_merged_df_spark
    .withColumn('PARTNER_STID', F.concat(F.lit('TESTID'), F.lpad(F.col('testID'), 10, '0')))
    .withColumnRenamed('findingCode', 'FINDING_CODE')
    .withColumnRenamed('findingStatusCd', 'FINDING_STATUS_CD')
)
df_model_output_filtered = (
    df_model_output_filtered
    .withColumn('PRESENT', F.lit(True))
)

### Merge the model output with the expected result on testpartnerID, findingCode and findingStatusCD
test_output = (
    output_input_merged_df_spark
    .join(df_model_output_filtered, ['PARTNER_STID', 'FINDING_CODE', 'FINDING_STATUS_CD'], 'left')
)

### Calculate the final Pass field and attach it to the final result
test_output = (
    test_output
    .withColumn('Pass',
        F.when(
            ((F.col('flag') & F.col('PRESENT')) |
            ((~F.col('flag')) & F.col('PRESENT').isNull())),
            F.lit(True)
        )
        .otherwise(F.lit(False))
    )
)

print('test_output', test_output.filter(F.col("Pass")).select("PARTNER_STID", "flag", "PRESENT", "Pass").show(truncate=False))

#### END NOTEBOOK CODE part 3

###### HERE ADD CODE TO SAVE REPORT IN ARTIFACTS

###### APPLY the assert HERE
# filter out the test case failing
test_output.show(truncate=False)
# test_output = test_output.filter(F.col("PARTNER_STID") != F.lit("TESTID0000000004"))
values_list = test_output.select("Pass").rdd.flatMap(lambda x: x).collect()
print("values_list",values_list)

csv_report_path_name = 'end2end_test_output_report.csv'
test_output.toPandas().to_csv(csv_report_path_name, index=False)
print(test_output)
assert False not in values_list
# or assert every value of Pass attribute are True

test_end2end_pipeline()