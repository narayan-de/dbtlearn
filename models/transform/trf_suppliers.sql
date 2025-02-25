{{config(materialized = 'table', schema = env_var('DBT_TRANSFORMSCHEMA', 'TRANSFORMING_DEV'))}}
 
select
  GET(XMLGET(suppliersinfo, 'SupplierID'), '$')::VARCHAR SupplierID
 ,GET(XMLGET(suppliersinfo, 'CompanyName'), '$')::VARCHAR CompanyName
 ,GET(XMLGET(suppliersinfo, 'ContactName'), '$')::VARCHAR ContactName
 ,GET(XMLGET(suppliersinfo, 'Address'), '$')::VARCHAR Address 
 ,GET(XMLGET(suppliersinfo, 'City'), '$')::VARCHAR City
 ,GET(XMLGET(suppliersinfo, 'PostalCode'), '$')::VARCHAR PostalCode
 ,GET(XMLGET(suppliersinfo, 'Country'), '$')::VARCHAR Country
from
{{ref('stg_suppliers')}}