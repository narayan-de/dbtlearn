{{config(materialized = 'table', schema = env_var('DBT_TRANSFORMSCHEMA', 'TRANSFORMING_DEV'))}}
 
select
p.ProductID,
p.ProductName,
c."CategoryName",
s.CompanyName as suppliercompany,
s.ContactName as suppliercontact,
s.city as suppliercity,
s.country as suppliercountry,
p.QuantityPerUnit,
p.UnitCost,
p.UnitPrice,
p.UnitsInStock,
p.UnitsOnOrder,
TO_DECIMAL(p.UnitPrice - p.UnitCost, 9 , 2 ) as profit,
IFF(p.UnitsOnOrder > p.UnitsInStock, 'Not Available', 'Available') as productavailability
from
{{ref('stg_products')}}  as p 
left join {{ref('trf_suppliers')}} as s
  on p.SupplierID= s.supplierid 
left join {{ref('lkp_categories') }} as c 
  on c.categoryid = p.CategoryID