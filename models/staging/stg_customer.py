import snowflake.snowpark.functions as F
def model(dbt, session):
    dbt.config(materialized = 'table')
    customers_df = dbt.source('RAW', 'raw_customers')
    return customers_df
 