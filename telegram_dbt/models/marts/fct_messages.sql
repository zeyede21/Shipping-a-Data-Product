select 
    id as message_id,
    date as date_day,  -- Keep this if needed
    date as date_id,   -- Add this to reference the date_id
    sender_id as channel_id,
    has_media,
    media_type,
    image_path
from {{ ref('stg_telegram_messages') }}