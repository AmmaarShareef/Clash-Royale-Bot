# yolo_test.py

from ultralytics import YOLO

# Load pretrained YOLOv8n model
model = YOLO("runs/detect/train2/weights/best.pt")

# Run inference on a test image
results = model("test/test6.png")  # results is a list of Results objects

for box in results[0].boxes:
    print(box)
