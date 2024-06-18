modelShoppingListTimestamp_dmy = businessDate
df_model_output_pd = model.interface_file.copy()
df_model_output_pd['SHOPPING_LIST_DATE'] = modelShoppingListTimestamp_dmy

df_model_output = spark.CreateDataFrame(df_model_output_pd.astype(str))

output_data_df = pd.read_csv(path_to_test_output_file)
output_input_merged_df = pd.merge(test_data_df, output_data_df, on='testID', how='inner')


test_partner_id_lits = [F.lit(x) for x in test_partner_ids]
model_output_keep_cols = ["PARTNER_STID", 'FINDING_CODE', 'FINDING_STATUS_CD']

df_model_output_filtered = (
    df_model_output
    .select(model_output_keep_cols)
    .filter(F.col('PARTNER_STID').isin(test_partner_id_lits))
)

spark = SparkSession.builder.getOrCreate()
output_input_merged_df_spark = spark.CreateDataFrame(output_input_merged_df)

output_input_merged_df_spark = (
    output_input_merged_df_spark
    .withColumn('PARTNER_STID', F.concat(F.lit('TESTID'), F.lpad(F.col('testID'), 10, '0')))
    .withColumnRenamed('findingCode', 'FINDING_CODE')
    .withColumnRenamed('findingStatus', 'FINDING_STATUS_CD')
)



df_model_output_filtered = (
    df_model_output_filtered
    .withColumn('PRESENT', F.lit(True))
)

test_output = (
    output_input_merged_df_spark
    .join(df_model_output_filtered, ['PARTNER_STID', 'FINDING_CODE', 'FINDING_STATUS_CD'], how='left')
)


test_output = (
    test_output
    .withColumn(
        'Pass',
        F.when(
            (F.col('flag') & F.col('PRESENT')) |
            (~F.col('flag') & ~F.col('PRESENT').isNull()),
            F.lit(True)
        )
        .otherwise(F.lit(False))
    )
)





from pyspark.sql import SparkSession
import pandas as pd
from pyspark.sql import functions as F

def create_spark_dataframe(model, businessDate):
    df_model_output_pd = model.interface_file.copy()
    df_model_output_pd['SHOPPING_LIST_DATE'] = businessDate
    spark = SparkSession.builder.getOrCreate()
    df_model_output = spark.createDataFrame(df_model_output_pd.astype(str))
    return df_model_output

def read_and_merge_data(path_to_test_output_file, test_data_df):
    output_data_df = pd.read_csv(path_to_test_output_file)
    output_input_merged_df = pd.merge(test_data_df, output_data_df, on='testID', how='inner')
    return output_input_merged_df

def filter_model_output(df_model_output, test_partner_ids):
    test_partner_id_lits = [F.lit(x) for x in test_partner_ids]
    model_output_keep_cols = ["PARTNER_STID", 'FINDING_CODE', 'FINDING_STATUS_CD']
    df_model_output_filtered = (
        df_model_output
        .select(model_output_keep_cols)
        .filter(F.col('PARTNER_STID').isin(test_partner_id_lits))
    )
    return df_model_output_filtered

def prepare_output_input_merged_df(output_input_merged_df):
    spark = SparkSession.builder.getOrCreate()
    output_input_merged_df_spark = spark.createDataFrame(output_input_merged_df)
    output_input_merged_df_spark = (
        output_input_merged_df_spark
        .withColumn('PARTNER_STID', F.concat(F.lit('TESTID'), F.lpad(F.col('testID'), 10, '0')))
        .withColumnRenamed('findingCode', 'FINDING_CODE')
        .withColumnRenamed('findingStatus', 'FINDING_STATUS_CD')
    )
    return output_input_merged_df_spark

def add_present_column(df_model_output_filtered):
    df_model_output_filtered = (
        df_model_output_filtered
        .withColumn('PRESENT', F.lit(True))
    )
    return df_model_output_filtered

def join_and_create_pass_column(output_input_merged_df_spark, df_model_output_filtered):
    test_output = (
        output_input_merged_df_spark
        .join(df_model_output_filtered, ['PARTNER_STID', 'FINDING_CODE', 'FINDING_STATUS_CD'], how='left')
    )
    test_output = (
        test_output
        .withColumn(
            'Pass',
            F.when(
                (F.col('flag') & F.col('PRESENT')) |
                (~F.col('flag') & ~F.col('PRESENT').isNull()),
                F.lit(True)
            )
            .otherwise(F.lit(False))
        )
    )
    return test_output