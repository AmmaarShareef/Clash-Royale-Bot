---

# **Clash-Royale-Bot**

Not really a full-fledged bot — just a simple helper that displays opponent elixir and possible cards in hand (which the game normally hides).

**Constraints:**

* Only trains 8 classes for now
* User's deck cannot contain duplicates from opponent’s
* Distinct and specific cards only

A **research-only experiment** for real-time card detection and elixir estimation.

---

## 🧩 Overview

Clash Royale Helper is a real-time **computer-vision tool** that:

* Detects opponent cards from screen captures
* Tracks their elixir usage
* Predicts rotation
* Displays the info in a simple GUI

**Not a bot.**
It does not automate gameplay or interact with the game in any way.
It only reads pixels and visualizes inferred state.

---

## 🎯 Core Features

### 🖼 Real-time screen capture (via `mss`)

* High-performance frame grabbing
* Low latency for live detection

### 📦 YOLO-based card detection

* YOLOv8 model trained on 8 card classes
* Confidence filtering
* 20+ frame stability checks to avoid false positives

### 🔢 Elixir estimation system

* +1 elixir every 2.8 seconds
* Subtracts elixir when a detected card is played
* Always clamped between 0–10

### 🔄 Opponent card rotation tracker

* Tracks hand, next cards, and full deck
* Uses `Counter` logic to infer current hand
* Rebuilds rotation using observed plays

### 🖥 Live GUI dashboard (Tkinter)

* Displays 4-card current hand
* Shows next predicted card
* Visual elixir bar
* Clean, minimal UI

### 🧵 Multiprocessing architecture

* `writer` → CV detection process
* `reader` → game logic + elixir engine
* GUI process runs independently
* Shared state using `multiprocessing.Manager`

---

## 🏗 Architecture

### **1. `amain.py`**

* Tkinter GUI
* Loads images
* Sets up multiprocessing
* Manages shared state
* Launches:

  * `writer()` from `card_det.py`
  * `reader()` from `elix_deck.py`

### **2. `card_det.py`**

* Screen capture via `mss`
* YOLO inference
* Confidence + frame-stability filtering
* Sends `{card_name, elixir_cost}` events through a queue

### **3. `elix_deck.py`**

* Elixir regeneration + subtraction
* Tracks deck and played cards
* Infers:

  * Current hand (4 cards)
  * Next card
* Writes final state into `shared_state`

---

## 🛠 Tech Stack

| Component           | Technology                           |
| ------------------- | ------------------------------------ |
| Real-time inference | YOLOv8                               |
| Screen capture      | mss                                  |
| GUI                 | Tkinter                              |
| Image processing    | Pillow (PIL)                         |
| Visualization       | OpenCV                               |
| Parallelism         | `multiprocessing.Process`            |
| Data structures     | `Manager().dict`, `Queue`, `Counter` |

---

## 📂 Folder Structure

```
Clash-Royale-Bot/
│
├── amain.py          # GUI + multiprocess controller
├── card_det.py       # YOLO detection engine
├── elix_deck.py      # Elixir & rotation logic
│
├── images/           # Card icons (PNG)
├── runs/             # YOLO training outputs
├── dataset/          # Training images / labels
└── README.md
```

---

## 🚀 How It Works Internally

1. **`writer()` detects a card**

   * YOLO processes each frame
   * If same class appears for ≥20 frames → confirmed play
   * Sends `{card, e_cost}` via queue

2. **`reader()` processes events**

   * Updates elixir with time delta
   * Subtracts elixir for detected card
   * Updates deck + rotation
   * Computes:

     * `curr_hand`
     * `next_card`
     * `opp_elixir`

3. **`amain.py` displays the state**

   * Elixir bar
   * 4-card hand
   * Next card

---

## ⚠️ Legal / Ethical Disclaimer

This project is strictly for:

* Research
* Personal learning
* Computer-vision experimentation

Forbidden uses:

* Commercial use
* Monetized services
* Cheating or violating Supercell's TOS
* Automation or controlling game input
* Selling derivative works

This project **does not automate gameplay**.

---

## 🤝 Credit / Attribution

If you use or modify this code, please credit **Ammaar Shareef**.
A simple line is enough:

**“Based on original Clash Royale Helper code by Ammaar Shareef.”**

---
