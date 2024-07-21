
class DataFrameProcessor:
    """
    A class used to generate the synthetic and legacy partner ids and mapping them together
    """

    def __init__(self, columns_to_convert, raw_repo_test_meta_dict, test_data_df, raw_repo):
        self.columns_to_convert = columns_to_convert
        self.raw_repo_test_meta_dict = raw_repo_test_meta_dict
        self.raw_repo = raw_repo
        self.test_data_df = test_data_df

    def convert_to_datetime(self, df, column, format):
        df[column] = df[column].astype(str)
        df[column] = pd.to_datetime(df[column], format=format)
        return df

    def convert_columns_to_datetime(self,, df, format):
        for column in self.columns_to_convert:
            df = self.convert_to_datetime(df, column, format)
        return df

    def filter_by_date(self, df, date_column, start_column, end_column):
        filter_df = df[date_column].between(df[start_column], df[end_column])
        return df.loc[filter_df]

    def filter_by_partner_ids(self, df, column, partner_ids):
        """
        Filter a DataFrame by partner IDs

        Parameters:
        column(str): the column in df with the partner IDs
        ids(list): The partner IDs to filter by
        """
        filter_df = df[column].isin(partner_ids)
        return df.loc[filter_df]

    def create_partner_dict(self, df, partner_column, legacy_column):
        partner_dict = {}
        for index, item in df.iterrows():
            partner_dict[item[partner_column]] = item[legacy_column]
        return partner_dict

def filter_dataframe_by_ids(self, df, ids, column_name):
    """
    Update the DataFrames in raw_repo with the new DataFrames from raw_repo_test_meta_dict.

    raw_repo_test_meta dict dictionary:
    keys: names of dataframes in raw_repo
    value: new DataFrame to replace the old one with
    """
    filter_df = df[column_name].isin(ids)
    return df.loc[filter_df]

def process_dataframes(self, filters):
    for column, values in filters.items():
        df = getattr(self.raw_repo, df_name)
        df_filter = self.filter_dataframe_by_ids(df, values, column)
        setattr(self.raw_repo, df_name, df_filter)

def update_raw_repo_dfs(self):
    """
    Update the DataFrames in raw_repo with the new DataFrames from raw_repo_test_meta_dict.

    raw_repo_test_meta dict dictionary:
    keys: names of dataframes in raw_repo
    value: "to append" keys where the values is a list of DataFrames to append to the existing DataFrame
    """
    for key in self.raw_repo_test_meta_dict.keys():
        setattr(self.raw_repo, key, self.raw_repo_test_meta_dict[key][rt_cols.new_df])

def update_append_raw_repo_dfs(self):
    """
    Append new DataFrames to the existing DataFrames in raw_repo.
    """
    for method in dir(self.raw_repo):
        if not method in self.raw_repo_test_meta_dict.keys():
            continue
        cur_df = getattr(self.raw_repo, method)
        if self.raw_repo_test_meta_dict[method][rt_cols.df_type] == KOALAS:
            cur_to_append = ks.concat(self.raw_repo_test_meta_dict[method][TO_APPEND])
            cur_df = ks.concat([cur_df, cur_to_append], ignore_index=True)
        else:
            cur_to_append = pd.concat(self.raw_repo_test_meta_dict[method][TO_APPEND])
            cur_df = pd.concat([cur_df, cur_to_append], ignore_index=True)
        self.raw_repo_test_meta_dict[method][rt_cols.new_df] = cur_df
    self.update_raw_repo_dfs()

def execute_steps(self):
    test_data_df = self.test_data_df
    
    test_data_df[rt_cols.NOW] = datetime.today().strftime('%Y-%m-%d')
    test_data_df = self.convert_columns_to_datetime(test_data_df, '%Y-%m-%d')
    
    test_data_df = self.filter_by_date(test_data_df, rt_cols.NOW, rt_cols.VALIDFROM, rt_cols.VALIDTO)
    
    synth_partner_ids = set(test_data_df[rt_cols.SYNTHPARTNERID])
    
    df_key_dir_filtered = self.filter_by_partner_ids(self.raw_repo.df_key_dir, rt_cols.partnerID, synth_partner_ids)
    legacy_partner_ids = set(df_key_dir_filtered[rt_cols.legacyPartnerID].tolist())
    
    synth_legacy_partner_df = df_key_dir_filtered.filter(items=[rt_cols.partnerID, rt_cols.legacyPartnerID]).drop_duplicates()
    synth_legacy_partner_dict = self.create_partner_dict(synth_legacy_partner_df, rt_cols.partnerID, rt_cols.legacyPartnerID)
    
    print("synth_partner_ids", synth_partner_ids)
    print("legacy_partner_ids", legacy_partner_ids)
    print("synth_legacy_partner_dict", synth_legacy_partner_dict)
    
    return test_data_df, df_key_dir_filtered, synth_legacy_partner_dict, synth_partner_ids, legacy_partner_ids

class DataTransformer:
    """
    A class for processing pandas DataFrames
    """
    def __init__(
        self,
        raw_repo,
        raw_repo_test_meta_dict,
        synth_partner_ids,
        legacy_partner_ids,
        test_data_df,
        test_changes_df,
        synth_legacy_partner_dict,
        dataframes_list,
        columns_to_convert
    ):
        self.raw_repo = raw_repo
        self.columns_to_convert = columns_to_convert
        self.raw_repo_test_meta_dict = raw_repo_test_meta_dict
        self.synth_partner_ids = synth_partner_ids
        self.legacy_partner_ids = legacy_partner_ids
        self.test_data_df = test_data_df
        self.test_changes_df = test_changes_df
        self.synth_legacy_partner_dict = synth_legacy_partner_dict
        self.test_partner_ids = []
        self.dataframes_list = dataframes_list
        for df_name in self.dataframes_list:
            for column in self.dataframes_list[df_name]:
                if self.dataframes_list[df_name][column]==rt_cols.synth_partner_ids:
                    self.dataframes_list[df_name][column] = self.synth_partner_ids
                elif self.dataframes_list[df_name][column]==rt_cols.legacy_partner_ids:
                    self.dataframes_list[df_name][column] = self.legacy_partner_ids

    def filter_dataframes(self):
        for df_name, filters in self.dataframes_list.items():
            for column, values in filters.items():
                df = getattr(self.raw_repo, df_name)
                dataframe_filter = DataFrameProcessor(self.columns_to_convert, self.raw_repo_test_meta_dict, self.test_data_df, self.raw_repo)
                filtered_df = dataframe_filter.filter_dataframe_by_ids(df, values, column)
                setattr(self.raw_repo, df_name, filtered_df)

    def update_raw_repo_dfs(self):
        """
        Updates DataFrames with new data
        """
        for key in self.raw_repo_test_meta_dict.keys():
            setattr(self.raw_repo, key, self.raw_repo_test_meta_dict[key][rt_cols.new_df])

    def update_append_raw_repo_dfs(self):
        """
        Append new data to existing DataFrames
        """
        for method in dir(self.raw_repo):
            if not method in self.raw_repo_test_meta_dict.keys():
                continue
            cur_df = getattr(self.raw_repo, method)
            if self.raw_repo_test_meta_dict[method][rt_cols.df_type] == KOALAS:
                cur_to_append = ks.concat(self.raw_repo_test_meta_dict[method][TO_APPEND])
                cur_df = ks.concat([cur_df, cur_to_append], ignore_index=True)
            else:
                cur_to_append = pd.concat(self.raw_repo_test_meta_dict[method][TO_APPEND])
                cur_df = pd.concat([cur_df, cur_to_append], ignore_index=True)
            self.raw_repo_test_meta_dict[method][rt_cols.new_df] = cur_df

    def process_test_data(self):
        for index, test_partner in self.test_data_df.iterrows():
            current_synthetic_id = test_partner[rt_cols.SYNTHPARTNERID]
            current_legacy_id = self.synth_legacy_partner_dict.get(current_synthetic_id)
            current_test_synthetic_id = rt_cols.TESTID + str(test_partner[rt_cols.testID]).zfill(10)
            current_test_legacy_id = rt_cols.TESTLEG + str(test_partner[rt_cols.testID]).zfill(9)
            self.test_partner_ids.append(current_test_synthetic_id)

        for method, actions in self.raw_repo_test_meta_dict.items():
            current_dataframe = getattr(self.raw_repo, method, None)
            if current_dataframe is None:
                continue
            logging.info(f'Working with df: {method}')
            for action in actions[ACTIONS]:
                field_id_to_replace = action[FIELD_ID_TO_REPLACE]
                logging.info(f'Working with action: {field_id_to_replace}')
                current_dataframe_id = getattr(current_dataframe, field_id_to_replace, None)
                if current_dataframe_id is None:
                    continue
                if action[rt_cols.PARTNER_ID_TO_USE] == SYNTH:
                    filter_condition = current_dataframe_id.isin([current_synthetic_id])
                    replacement_id = current_test_synthetic_id
                else:
                    filter_condition = current_dataframe_id.isin([current_legacy_id])
                    replacement_id = current_test_legacy_id
                record_to_copy = current_dataframe.loc[filter_condition].copy()
                record_to_copy[field_id_to_replace] = replacement_id
                actions[TO_APPEND].append(record_to_copy)
        self.update_append_raw_repo_dfs()
        print("test_partner_ids", self.test_partner_ids)
        return self.test_partner_ids

    def execute_all_steps(self):
        self.filter_dataframes()
        self.process_test_data()
        return self.test_partner_ids

    def process_test_changes(self):
        """
        Processes the changes in the test data

        Parameters:
        test_changes_df_merged : DataFrame
        synth_legacy_partner_dict : a dictionary that contains the synthetic legacy partner ids
        """
        test_changes_df_merged = pd.merge(self.test_changes_df, self.test_data_df, on='testID', how='inner')
        for index, test_change in test_changes_df_merged.iterrows():
            logging.info(f'Working with test ID: {str(test_change[rt_cols.testID])}')
            cur_synth_id = test_change[rt_cols.SYNTHPARTNERID]
            cur_legacy_id = self.synth_legacy_partner_dict.get(cur_synth_id)
            cur_test_synth_id = rt_cols.TESTID + str(test_change[rt_cols.testID]).zfill(10)
            cur_test_legacy_id = rt_cols.TESTLEG + str(test_change[rt_cols.testID]).zfill(9)
            logging.info(f'Working with df: {test_change[DATAFRAME]}')
            cur_df = getattr(self.raw_repo, test_change[DATAFRAME])
            cur_field_to_replace = test_change[COLUMN_NAME]
            cur_field_id = self.raw_repo_test_meta_dict[test_change[DATAFRAME]][ID]
            cur_df_id = getattr(cur_df, cur_field_id)
            cur_field_pk_list = self.raw_repo_test_meta_dict[test_change[DATAFRAME]][PK]
            cur_df_pk_list = [getattr(cur_df, pk) for pk in cur_field_pk_list]
            key_value_list = test_change['keyValue'].split(',')
            logging.info(f'key_value_list: {key_value_list}')
            if self.raw_repo_test_meta_dict[test_change[DATAFRAME]][rt_cols.TYPE] == SYNTH:
                cur_filter = cur_df_id.isin([cur_test_synth_id])
                print("cur df id isin cur_test_synth_id", cur_filter)
                for index, pk_column in enumerate(cur_df_pk_list):
                    cur_cond = pk_column.isin([key_value_list[index]])
                    cur_filter = cur_filter & cur_cond
                cur_df.loc[cur_filter, cur_field_to_replace] = test_change[rt_cols.VALUE]
            else:
                cur_filter = cur_df_id.isin([cur_test_legacy_id])
                for index, pk_column in enumerate(cur_df_pk_list):
                    cur_cond = pk_column.isin([key_value_list[index]])
                    cur_filter = cur_filter & cur_cond
                cur_df.loc[cur_filter, cur_field_to_replace] = test_change[rt_cols.VALUE]
            self.raw_repo_test_meta_dict[test_change[DATAFRAME]][rt_cols.new_df] = cur_df
        self.update_raw_repo_dfs()

class ShoppingDataProcessor:
    """
    Process shopping list by applying include/exclude rules and logging the results

    Output:
    A tuple containing two pandas Series: partner_ids_in_scope and partner_ids_out_of_scope
    """
    def __init__(self, raw_repo, shopping_list_processing, technical_config, not_anymore_clients):
        self.raw_repo = raw_repo
        self.shopping_list_processing = shopping_list_processing
        self.technical_config = technical_config
        self.not_anymore_clients = not_anymore_clients

    def process_shopping_list(self):
        shopping_list = pd.Series(list(self.raw_repo.df.pich.PARTNER_ID.unique()), name=rt_cols.PARTNER_ID)
        print(f"shopping_list_value_counts:", shopping_list.value_counts())
        self.raw_repo.load_shopping_list_info(date=self.technical_config.exec_config.CALCULATION_DATE, partner_ids=shopping_list)

        partner_ids_in_scope, partner_ids_out_of_scope = self.shopping_list_processing.apply_include_exclude_rules(self.raw_repo.df_shopping_list_info)

        partner_ids_in_scope = partner_ids_in_scope.drop_duplicates()
        partner_ids_out_of_scope = partner_ids_out_of_scope.drop_duplicates()

        partner_ids_in_scope = partner_ids_in_scope[~partner_ids_in_scope.isin(partner_ids_out_of_scope)]

        scope_ids = list(partner_ids_in_scope) + list(partner_ids_out_of_scope)
        legal_entities_and_old_clients = [id for id in shopping_list if id not in scope_ids] + list(self.not_anymore_clients)

        partner_ids_out_of_scope = pd.concat([partner_ids_out_of_scope, pd.Series(legal_entities_and_old_clients)])

        logging.info(f'IN SCOPE POP: {len(partner_ids_in_scope)}')
        logging.info(f'OUT OF SCOPE POP: {len(partner_ids_out_of_scope)}')

        print(f'IN SCOPE POP: {len(partner_ids_in_scope)}')
        print(f'OUT OF SCOPE POP: {len(partner_ids_out_of_scope)}')

        return partner_ids_in_scope, partner_ids_out_of_scope


class EvaluateModel:
    """
    Evaluate a model based on the processed data.

    Raw data mapped to a new format.
    Checks the data.
    Evaluate the model.
    """
    def __init__(self, raw_repo, technical_config, partner_ids_in_scope, partner_ids_out_of_scope):
        self.raw_repo = raw_repo
        self.technical_config = technical_config
        self.partner_ids_in_scope = partner_ids_in_scope
        self.partner_ids_out_of_scope = partner_ids_out_of_scope

    def process_data_and_evaluate_model(self):
        AuthoritativeDataMapper.use_koalas()
        print("all_partner_ids", self.raw_repo.all_partner_ids.count())
        print("df_busra", self.raw_repo.df_busra.count())
        print("df_advisor", self.raw_repo.df_advisor.count())
        print("df_contract", self.raw_repo.df_contract.count())
        data_repo = AuthoritativeDataMapper.map_data(self.raw_repo,
                                                     self.technical_config.exec_config,
                                                     self.partner_ids_in_scope,
                                                     self.partner_ids_out_of_scope)

        data_repo.partner_scope = {"IN": self.partner_ids_in_scope, "OUT": self.partner_ids_out_of_scope}
        print("data_repo partner_scope count", data_repo.partner_scope)

        data_repo.prepare_data()
        model = Review(self.technical_config.exec_config)
        print("model data", model.data)
        model_indicators = IndicatorsRepo(model.data)
        print("model indicators", model_indicators)
        model_scenarios = ScenariosRepo(model_indicators)
        print("model scenarios", model_scenarios)
        model_checks = Datachecker(data_repo)
        model_checks.complete_check()
        model.evaluate_modules()

        return model


class ModelProcessor:
    """
    Provides methods to modify the model's interface file.
    Read and merge output data
    Filter the model output
    Create a test output DataFrame and provide columns "PRESENT" and "PASS" based on certain conditions
    """
    def __init__(self, model, businessDate, test_data_df, output_data_df, test_partner_ids):
        self.model = model
        self.businessDate = businessDate
        self.test_data_df = test_data_df
        self.output_data_df = output_data_df
        self.test_partner_ids = test_partner_ids

    def create_model_output_dataframe(self):
        df_model_output_pd = self.model.interface_file.copy()
        print("df_model_output_pd step0", df_model_output_pd.count())
        print("df_model_output_pd step0", df_model_output_pd)

        df_model_output_pd[rt_cols.SHOPPING_LIST_DATE] = self.businessDate
        df_model_output_pd.shopping_list_date = df_model_output_pd[SHOPPING_LIST_DATE]

        spark = SparkSession.builder.getOrCreate()
        df_model_output = spark.createDataFrame(df_model_output_pd.astype(str))
        print("df_model_output", df_model_output.count())
        print("df_model_output", df_model_output)

        return df_model_output

    def output_input_merge_df(self):
        df_output_input_merged_df = pd.merge(self.test_data_df, self.output_data_df, on=rt_cols.testID, how='inner')
        print("output_input_merged_df", len(output_input_merged_df))
        print("output_input_merged_df flag true count", output_input_merged_df['flag'].sum())
        return output_input_merged_df

    def filter_model_output(self):
        test_partner_ids_lits = F.lit(x) for x in self.test_partner_ids
        model_output_keep_cols = [rt_cols.PARTNER_STID, rt_cols.FINDING_CODE, rt_cols.FINDING_STATUS_CD]

        df_model_output = self.create_model_output_dataframe()
        print("df_model_output", df_model_output.count())
        df_model_output_filtered = (
            df_model_output
            .filter(F.col(rt_cols.PARTNER_STID).isin(test_partner_ids_lits))
            .select(model_output_keep_cols)
        )

        print("test_partner_ids_lits", test_partner_ids_lits)
        print("df_model_output_filtered", df_model_output_filtered.count())
        print("df_model_output_filtered groupby partner_stid count", df_model_output_filtered.groupby(rt_cols.PARTNER_STID).count().show())

        return df_model_output_filtered


    def prepare_output_input_merged_df(self):
        spark = SparkSession.builder.getOrCreate()
        output_input_merged_df = self.output_input_merge_df()
        output_input_merged_df_spark = spark.createDataFrame(output_input_merged_df)
        output_input_merged_df_spark = (
            output_input_merged_df_spark
            .withColumn(rt_cols.PARTNER_STID, F.concat(F.lit(rt_cols.TESTID), F.lpad(F.col(rt_cols.testID), 10, '0')))
            .withColumnRenamed(rt_cols.findingCode, rt_cols.FINDING_CODE)
            .withColumnRenamed(rt_cols.findingStatusCD, rt_cols.FINDING_STATUS_CD)
        )
        return output_input_merged_df_spark

    def add_present_column(self):
        df_model_output_filtered = self.filter_model_output()
        df_model_output_filtered = (
            df_model_output_filtered
            .withColumn(rt_cols.PRESENT, F.lit(True))
        )
        return df_model_output_filtered

    def join_and_create_pass_column(self):
        output_input_merged_df_spark = self.prepare_output_input_merged_df()
        df_model_output_filtered = self.add_present_column()
        test_output = (
            df_model_output_filtered
            .join(output_input_merged_df_spark, [rt_cols.PARTNER_STID, rt_cols.FINDING_CODE, rt_cols.FINDING_STATUS_CD], how='left')
        )
        test_output = (
            test_output
            .withColumn(
                rt_cols.Pass,
                F.when(
                    (F.col(rt_cols.flag) & F.col(rt_cols.PRESENT)) |
                    (F.col(rt_cols.flag) & F.col(rt_cols.PRESENT).isNull()),
                    F.lit(True)
                ).otherwise(F.lit(False))
            )
        )
        print('test_output:', test_output.filter(F.col("Pass")).select("PARTNER_STID", "flag", "PRESENT", "Pass").show(truncate=False))

    def execute_all_steps(self):
        test_output = self.join_and_create_pass_column()
        print('test_output:', test_output.filter(F.col("Pass")).select("PARTNER_STID", "flag", "PRESENT", "Pass").show(truncate=False))
        return test_output




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

not_anymore_clients = [x for x in original_shopping_list if (x not in df_pich.PARTNER_ID.unique())]

# We need to remove PARTNER_ID if in the list of any reason
not_anymore_clients = [x for x in not_anymore_clients if x != 'PARTNER_ID']
raw_repo.df_pich = df_pich

def main():
    path_to_test_input_file = path_input_test_cases_end2end_pipeline + "/skr_test_input.csv"
    path_to_test_changes_file = path_input_test_cases_end2end_pipeline + "/skr_test_changes.csv"
    path_to_test_output_file = path_input_test_cases_end2end_pipeline + "/skr_test_output.csv"

    test_data_df = pd.read_csv(path_to_test_input_file)
    test_changes_df = pd.read_csv(path_to_test_changes_file)
    output_data_df = pd.read_csv(path_to_test_output_file)

    dataframe_processor = DataFrameProcessor(columns_to_convert, raw_repo_test_meta_dict, test_data_df, raw_repo)
    test_data_df, df_key_dir_filtered, synth_legacy_partner_dict, synth_partner_ids, legacy_partner_ids = (
        dataframe_processor.execute_steps()
    )

    data_transformer_processor = DataTransformer(
        raw_repo,
        raw_repo_test_meta_dict,
        synth_partner_ids,
        legacy_partner_ids,
        test_data_df, test_changes_df, synth_legacy_partner_dict, dataframes_list, columns_to_convert
    )
    test_partner_ids = data_transformer_processor.execute_all_steps()
    data_transformer_processor.process_test_changes()

    shopping_data_processor = ShoppingDataProcessor(raw_repo, shopping_list_processing, technical_config, not_anymore_clients)
    partner_ids_in_scope, partner_ids_out_of_scope = shopping_data_processor.process_shopping_list()

    evalue_model_processor = EvaluateModel(raw_repo, technical_config, partner_ids_in_scope, partner_ids_out_of_scope)
    model = evalue_model_processor.process_data_and_evaluate_model()

    model_processor = ModelProcessor(model, business_date, test_data_df, output_data_df, test_partner_ids)
    output = model_processor.execute_all_steps()

main()