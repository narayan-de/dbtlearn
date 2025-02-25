import snowflake.snowpark.functions as f 

def model(dbt, session):
    dbt.config(materialized = 'table',schema='trf_dev')

    shipments_df = dbt.ref('shipment_snapshot')
    shippers_df = dbt.ref('lkp_shippers')

    final_shipments_df = (
                            shipments_df
                            . join(shippers_df, shipments_df.shipperid == shippers_df.SHIPPERID, 'left')
                            .select(
                                shipments_df.orderid,
                                shipments_df.lineno,
                                shipments_df.shipmentdate,
                                shipments_df.status,
                                shippers_df.companyname
                            )
    )

    final_shipments_df = final_shipments_df.filter(f.col('dbt_valid_to').isNull())

    return final_shipments_df
