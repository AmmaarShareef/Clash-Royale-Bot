# yolo_test.py

from ultralytics import YOLO

# Load pretrained YOLOv8n model
model = YOLO("yolov8n.pt")

# Run inference on a test image
results = model("Dataset/sarah.jpeg")  # results is a list of Results objects

# Show results for each image
for r in results:
    r.show()  # now works