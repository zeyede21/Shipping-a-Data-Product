select distinct 
    sender_id as channel_id  -- Use 'sender_id' as the unique identifier for channels
from {{ ref('stg_telegram_messages') }}