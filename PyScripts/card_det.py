# card_det.py

import json, random, time, os

import cv2
import numpy as np
import mss

from ultralytics import YOLO

model = YOLO("runs/detect/train2/weights/best.pt")

elix = 0
card_indx = 0
last_card = 0
cls_id = 0

cards_played = 0
frame_val = 0

cards = [
  { "card": "minipekka",        "e_cost": 4 },
  { "card": "fireball",        "e_cost": 4 },
  { "card": "musk",         "e_cost": 4 },
  { "card": "giant",            "e_cost": 5 },
  { "card": "minions",          "e_cost": 3 },
  { "card": "knight",      "e_cost": 3 },
  { "card": "archers",       "e_cost": 3 },
  { "card": "goblins",             "e_cost": 2 }
]

def writer(q): #everything needs to run inside this so amain.py can run this entire processw
    global last_card, frame_val, cls_id
    
    with mss.mss() as sct:
        monitor = {"top": 0, "left": 832, "width": 860, "height": 1600}

        while "Screen capturing":
            last_time = time.time()

            img = np.array(sct.grab(monitor)) # raw pixel data needs to be converted to an image using numpy
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR) # convert to RGB for YOLOv8

            results = model(img, verbose=False)
            annotated = results[0].plot()

            cv2.imshow("Detection preview", annotated)

            # Getting class id (index) from boxes, an array returned from results[0]
            boxes = results[0].boxes

            if len(boxes) > 0:
                best_idx = int(boxes.conf.argmax()) # returns class index (in boxes) with highest confidence
                if float(boxes[best_idx].conf) > 0.65: # if confidence score above 70% then select
                    cls_id = int(boxes[best_idx].cls) # use class id with highest confidence

            if last_card == cls_id:
                frame_val += 1
            else:
                frame_val = 0
            last_card = cls_id

            if frame_val >= 60: # if card has been detected consistently for more than 30 frames
                q.put(cards[cls_id])

            # Press "q" to quit
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break
