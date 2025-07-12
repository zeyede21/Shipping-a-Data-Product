-- models/staging/stg_telegram_messages.sql
with raw as (
   select *
     from raw.telegram_messages
)
select id,
       date,
       sender_id,
       text,
       has_media,
       media_type,
       image_path,
       channel,
       length(text) as message_length
  from raw