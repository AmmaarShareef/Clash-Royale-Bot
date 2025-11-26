# elix_deck.py

import time
from collections import Counter

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
curr_hand = [] # Current usable deck of 4
next_cards = [" ", " ", " ", " "] # The next possible card (one of these 4)
last_card = ""

def subElix(cost):
    global opp_elixir
    if opp_elixir >= cost:
        opp_elixir -= cost
        
def reader(q, shared_state):
    global last_time, last_elix, opp_elixir, last_card, next_cards, curr_hand, opp_deck
    item = {"card": "nocard", "e_cost": 0}  # default
    
    while game_run:

        if not q.empty():
            item = q.get() # fetch card state
        
        now = time.perf_counter()
        sec_elapsed = now - last_time

        opp_elixir += (sec_elapsed / elx_gen_time) # Calc. elixir by time passed / 2.8 (if 2.8s passed then +1 elixir)
        opp_elixir = min(opp_elixir, 10) # Clamping, elixir will go above 10, but min will choose 10 and run it again

        last_time = now # When 'now' is calculated (next loop), some time (0.1s) would have passed since last_time

        # Print Control
        curr_elix = int(opp_elixir)
        if curr_elix != last_elix:
            print(curr_elix)
            last_elix = curr_elix

        card = item.get("card")    

        if card != last_card:
            print(card)
            # Sub elixir 
            to_sub = item["e_cost"]
            subElix(to_sub)
            # Add to next card, will come back after 3 cycles
            next_cards.pop(0)
            next_cards.append(card)
            # Add placed card to opp_deck if not already there
            if card not in opp_deck and card != "nocard":
                opp_deck.append(card)
            last_card = card
            curr_hand = list((Counter(opp_deck) - Counter(next_cards)).elements()) # Whatever isnt in next_cards is in the curr_hand
            
        shared_state["opp_elixir"] = int(opp_elixir)
        shared_state["curr_hand"] = curr_hand
        shared_state["next_cards"] = next_cards


        time.sleep(0.01) # Reducing CPU load by limiting loop to 1 times / second