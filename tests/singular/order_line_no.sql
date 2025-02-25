select orderid,count(distinct lineno)
from
{{ref('fct_orders')}}
group by orderid
having count(distinct lineno) = 0

