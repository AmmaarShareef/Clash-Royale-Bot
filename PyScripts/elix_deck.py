# elix_deck.py

import time, keyboard, json
import os

# Time
last_time = time.perf_counter()
now = 0
sec_elapsed = 0

# Game control
game_run = True

# Elixir
opp_elixir = 10 # Starting elixir every match
elx_gen_time = 2.8 # 1 elixir per 2.8s
last_elix = 0 # To avoid multiple prints of current elixir
to_sub = 0 # Elixir Cost

# Deck
opp_deck = [] # Full 8 card deck
possible4 = [] # The next possible card (one of these 4)
curr_hand = [] # Current usable deck of 4
last_card = ""

def subElix():
    global opp_elixir
    if opp_elixir >= to_sub:
        opp_elixir -= to_sub 
        
#keyboard.on_release_key("space", subElix)

tmp = "Card_State.txt.tmp"
final = "Card_State.txt"

# Clean card_state by writing to a temporary file
with open(tmp, "w") as f:
    f.write(json.dumps({"card": "nocard", "e_cost": 0 }))
    
os.replace(tmp, final) # Atomic move, txt file is never empty, using os its state instantly updated.

while game_run:
    
    now = time.perf_counter()
    sec_elapsed = now - last_time
    
    opp_elixir += (sec_elapsed / elx_gen_time) # Calc. elixir by time passed / 2.8 (if 2.8s passed then +1 elixir)
    opp_elixir = min(opp_elixir, 10) # Clamping, elixir will go above 10, but min will choose 10 and run it again
    
    last_time = now # When 'now' is calculated (next loop), some time (0.1s) would have passed since last_time
    
    # Print Control
    curr_elix = int(opp_elixir)
    if curr_elix != last_elix:
        print(curr_elix, opp_deck)
        last_elix = curr_elix
    
    # Read Card Detection File and collect JSON object
    with open("Card_State.txt", "r") as f:
        info = json.loads(f.read())
        card = info.get("card")
        if card != last_card:
            # Sub elixir 
            to_sub = info["e_cost"]
            subElix()
            # Add placed card to opp_deck if not already there
            if card not in opp_deck:
                opp_deck.append(card)
            last_card = card

    
    time.sleep(0.1) # Reducing CPU load by limiting loop to 10 times / second