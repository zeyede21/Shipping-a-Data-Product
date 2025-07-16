from ultralytics import YOLO
import os
import pandas as pd

# Initialize model (downloads if not available)
model = YOLO("yolov8n.pt")  # You can also try yolov8m.pt or yolov8s.pt for better accuracy

# Directory path to scan
image_base_dir = r"D:\10Academy1\Shipping-a-Data-Product\data\raw\images\2025-07-12"

results = []

for channel in os.listdir(image_base_dir):
    channel_path = os.path.join(image_base_dir, channel)
    if not os.path.isdir(channel_path):
        continue

    for file in os.listdir(channel_path):
        if file.endswith(".jpg"):
            image_path = os.path.join(channel_path, file)
            detections = model(image_path)[0]

            for det in detections.boxes:
                results.append({
                    "channel_name": channel,
                    "image_file": file,
                    "detected_object_class": model.names[int(det.cls)],
                    "confidence_score": round(float(det.conf), 3)
                })


# Save detection results to CSV (optional intermediate step)
df = pd.DataFrame(results)
df.to_csv(r"D:\10Academy1\Shipping-a-Data-Product\data\raw\images\2025-07-12\yolo_detections.csv", index=False)
print("Saved detections to yolo_detections.csv")
