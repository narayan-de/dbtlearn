{{config(materialized = 'table')}}

select *
from 
{{source('RAW','raw_employees')}}
