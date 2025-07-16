 (
    SELECT
        yd.channel_name,
        yd.image_file,
        yd.detected_object_class,
        yd.confidence_score
    FROM {{ source('zeyede', 'yolo_detections') }} yd
)