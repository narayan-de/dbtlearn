{{ config(materialized = 'incremental', unique_key = ['orderid','lineno']) }}

select od.*,o.order_date
from
{{source('RAW', 'raw_order_details')}} as od inner join
{{source('RAW', 'raw_orders')}} as o on od.orderid = o.orderid

{% if is_incremental() %}
 
where o.order_date > (select max(order_date) from {{this}} )
 
{% endif %}