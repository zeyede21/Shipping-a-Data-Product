select distinct 
    date as date_id,  -- Use 'date' from the message
    extract(week from date) as week,
    extract(month from date) as month,
    extract(year from date) as year
from {{ ref('stg_telegram_messages') }}