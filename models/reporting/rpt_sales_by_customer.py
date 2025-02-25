import snowflake.snowpark.functions as F
import pandas as pd
import holidays

def avgordervalue(nooforders, totalvalue):
    return totalvalue/nooforders

def is_holiday(holiday_date):
    French_holidays = holidays.France()
    FrenchHoliday = (holiday_date in French_holidays)
    return FrenchHoliday

def model(dbt, session):
    dbt.config(materialized = 'table', schema = 'reporting_dev', packages=["holidays"])

    orders_df = dbt.ref('fct_orders')
    orders_agg_df = (
                    orders_df
                    .group_by('customerid')
                    .agg
                    (
                        F.min(F.col('order_date')).alias('First_Order_Date'),
                        F.max(F.col('order_date')).alias('Recent_Order_Date'),
                        F.count(F.col('orderid')).alias('Total_Orders'),
                        F.countDistinct(F.col('productid')).alias('No_Of_Products'),
                        F.sum(F.col('quantity')).alias('Total_Quantity'),
                        F.sum(F.col('linesalesamount')).alias('Total_Sales'),
                        F.avg(F.col('margin')).alias('Avg_Margin')
                    )
                )
 
    customer_df = dbt.ref('dim_customers')
 
    customer_order_df = (
                            customer_df
                            .join(orders_agg_df, orders_agg_df.customerid == customer_df.customerid, 'left')
                            .select(customer_df.companyname,
                                    customer_df.contactname,
                                    orders_agg_df.First_Order_Date,
                                    orders_agg_df.Recent_Order_Date,
                                    orders_agg_df.Total_Orders,
                                    orders_agg_df.No_Of_Products,
                                    orders_agg_df.Total_Quantity,
                                    orders_agg_df.Total_Sales,
                                    orders_agg_df.Avg_Margin
                                    )
    )    

    cutomer_order_final_df = customer_order_df.withColumn('AvgOrderAmount',avgordervalue(customer_order_df["Total_Quantity"],customer_order_df["Total_Sales"]))

    final_df = cutomer_order_final_df.filter(F.col('FIRST_ORDER_DATE').isNotNull())

    final_orders_df = final_df.to_pandas()
   
    final_orders_df["is_first_order_on_holiday"] = final_orders_df["FIRST_ORDER_DATE"].apply(is_holiday)
 
    return final_orders_df