import snowflake.snowpark.functions as F
def model(dbt, session):
    dbt.config(materialized = 'table')
    products_df = dbt.source('RAW', 'raw_products')
    return products_df
 