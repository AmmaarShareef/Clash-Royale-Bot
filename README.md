# Clash-Royale-Bot

Not really a full fledged bot, a simple helper that displays opponent elixir and possible cards in hand, which is not displayed usually.

Constraints:

- Only train 8 classes as of now.
- User's deck can't contain any duplicates from opponents to avoid any disruption.
- Distinct and specific cards

Clash Royale Helper — Computer-Vision Powered Card & Elixir Tracker

A research-only experiment for real-time card detection and elixir estimation.

🧩 Overview

Clash Royale Helper is a real-time computer-vision tool that detects opponent cards from screen captures, tracks their elixir usage, predicts rotation, and displays the information in a small GUI.

It is not a bot, does not automate gameplay, and does not interact with the game.
It only reads pixels, infers information, and visualizes card state — intended strictly for learning, research, and experimentation.

🎯 Core Features

🖼 Real-time screen capture (via mss)

📦 YOLO-based card detection

Runs a local YOLOv8 model trained on 8 card classes

Filters predictions by confidence

Debounces via frame consistency checks (20+ frames)

🔢 Elixir estimation system

+1 elixir every 2.8s

Elixir subtraction on detected card plays

Clamped between 0–10

🔄 Opponent card rotation tracker

Tracks hand, next cards, and full discovered deck

Uses Counter math to infer the current 4-card hand from known next cards

🖥 Live GUI dashboard (Tkinter)

Current hand (4 slots)

Next card prediction

Elixir bar (0–10)

Clean gradient UI

🧵 Multiprocessing architecture

writer → CV detection process

reader → game logic + elixir engine

GUI process runs independently

Shared state via multiprocessing.Manager

🏗 Architecture

1. amain.py

Handles:

Tkinter GUI rendering

Image loading

Multiprocessing setup

Shared state dictionary

Launches:

writer() from card_det.py

reader() from elix_deck.py

2. card_det.py

Responsible for:

Screen capture (MSS)

YOLO inference

Confidence thresholding

Frame-stability logic

Sending detected cards (+ elixir cost) into a queue for processing

3. elix_deck.py

Handles game logic:

Elixir regeneration

Subtracting elixir on card play

Deck tracking

Hand rotation inference

Writes final state into shared_state for the GUI

🛠 Tech Stack
Component Technology
Real-time inference YOLOv8 (Ultralytics)
Screen capture mss
GUI Tkinter
Image work Pillow (PIL)
Visualization OpenCV
Parallelism multiprocessing.Process
Data structures Manager().dict, Queue, Counter
📂 Folder Structure
Clash-Royale-Bot/
│
├── amain.py # GUI + multiprocess controller
├── card_det.py # YOLO detection engine
├── elix_deck.py # Elixir & card rotation logic
│
├── images/ # Card icons (PNG)
├── runs/ # YOLO training outputs
├── dataset/ # Training images / labels
└── README.md

🚀 How It Works Internally

writer() detects a card

YOLO processes each frame

If the same class is detected for ≥20 frames → considered a real play

Sends { card: name, e_cost: X } through a multiprocessing queue

reader() receives card events

Updates elixir based on time delta

Subtracts elixir for the detected card

Updates deck

Calculates:

curr_hand (4-card hand)

next_cards (rotation)

opp_elixir

amain.py GUI displays everything

Shows elixir bar

Shows 4 current cards

Shows next card

⚠️ Legal / Ethical Disclaimer

This project is strictly for:

✔ Research
✔ Personal learning
✔ Computer-vision experimentation

You may not use this code for:

❌ Commercial products

❌ Monetized services

❌ Cheating, automation, or violating Supercell's TOS

❌ Selling derivative works

This project does not control the game and must not be used to automate gameplay in any form.

🤝 Credit / Attribution

If you use, modify, or build on this code:

Please provide clear attribution to Ammaar Shareef
(e.g., in your README, documentation, or academic report)

A simple line is enough:

Based on original Clash Royale Helper code by Ammaar Shareef.
