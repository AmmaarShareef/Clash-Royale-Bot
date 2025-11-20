# card_det.py

import json, random, time

import cv2
import numpy as np
import mss

from ultralytics import YOLO

model = YOLO("runs/detect/train2/weights/best.pt")

with mss.mss() as sct:
    monitor = {"top": 0, "left": 832, "width": 860, "height": 1600}
    
    while "Screen capturing":
        last_time = time.time()
        
        img = np.array(sct.grab(monitor)) # raw pixel data needs to be converted to an image using numpy
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR) # convert to RGB for YOLOv8
        
        results = model(img, verbose=False)
        annotated = results[0].plot()
        
        cv2.imshow("Detection preview", annotated)
        
        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
        
'''
elix = 0

card_indx = 0
cards_played = 0
cards = [
  { "card": "Skeletons",        "e_cost": 1 },
  { "card": "Berserker",        "e_cost": 2 },
  { "card": "Musketeer",         "e_cost": 3 },
  { "card": "Fireball",            "e_cost": 4 },
  { "card": "Wizard",          "e_cost": 5 },
  { "card": "Royal Giant",      "e_cost": 6 },
  { "card": "Mega Knight",       "e_cost": 7 },
  { "card": "Golem",             "e_cost": 8 }
]

model = YOLO("yolov8n.pt")  # loads a small pretrained model
model.info() # prints model details

while True:
    card_indx = random.randint(0, len(cards)-1)
    cards_played += 1
    
    with open("Card_State.txt", "w") as f:
        f.write(json.dumps(cards[card_indx]))
    
    # So it doesnt just keep updating card state rapidly
    time.sleep(5) #cards[card_indx]["e_cost"] / 2
'''