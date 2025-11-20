# yolo_test.py

from ultralytics import YOLO
import torch

# Load pretrained YOLOv8n model
model = YOLO("runs/detect/train2/weights/best.pt")

# Run inference on a test image
results = model("test14.png")  # results is a list of Results objects

# Show results for each image
for r in results:
    r.show()  # now works
