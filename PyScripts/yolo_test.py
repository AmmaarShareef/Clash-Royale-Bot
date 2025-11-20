# yolo_test.py

from ultralytics import YOLO

# Load pretrained YOLOv8n model
model = YOLO("runs/detect/train2/weights/best.pt")

# Run inference on a test image
results = model("test14.png")  # results is a list of Results objects

results.show()  # now works
