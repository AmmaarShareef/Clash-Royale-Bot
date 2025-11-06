# card_det.py

import json, random, time
from ultralytics import YOLO

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
