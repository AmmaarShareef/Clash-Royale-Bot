# amain.py

from multiprocessing import Process, Queue, Manager
from card_det import writer
from elix_deck import reader
import tkinter as tk
from PIL import Image, ImageTk
import os

# -------------------------
# CARD IMAGE SIZE (EDIT THIS ONLY)
# -------------------------
CARD_SIZE = 65
# -------------------------


# ---- GUI function ----
def run_gui(shared_state, images_dir, card_names):

    root = tk.Tk()
    root.title("Clash Royale Helper Display")
    root.geometry("400x320")

    # base bg
    root.configure(bg="black")

    # ---- gradient background ----
    gradient = tk.Canvas(root, width=400, height=320, highlightthickness=0, bg="black")
    gradient.place(x=0, y=0)

    for i in range(320):
        r = 25
        g = 0
        b = 60 + int(i * 0.25)
        color = f"#{r:02x}{g:02x}{b:02x}"
        gradient.create_line(0, i, 400, i, fill=color)

    # ---- LOAD & RESIZE IMAGES ----
    card_images = {}
    full_list = card_names + ["qmark"]

    for name in full_list:
        fp = os.path.join(images_dir, f"{name}.png")
        print("Loading:", fp)
        try:
            pil = Image.open(fp).resize((CARD_SIZE, CARD_SIZE), Image.LANCZOS)
            card_images[name] = ImageTk.PhotoImage(pil)
        except Exception as e:
            print("FAILED:", fp, e)
            card_images[name] = None

    # ---- Elixir Bar ----
    elixir_canvas = tk.Canvas(root, width=300, height=20, bg="black",
                              highlightthickness=0)
    elixir_canvas.pack(pady=5)

    # ---- Current Hand Title ----
    hand_title = tk.Label(root, text="Current Hand",
                          font=("Arial", 12, "bold"),
                          fg="white", bg="black")
    hand_title.pack()

    # ---- Hand Frame ----
    hand_frame = tk.Frame(root, bg="black")
    hand_frame.pack(pady=5)

    # start with qmark in all 4 slots
    hand_labels = []
    for _ in range(4):
        lbl = tk.Label(hand_frame, image=card_images["qmark"], bg="black")
        lbl.image = card_images["qmark"]
        lbl.pack(side=tk.LEFT, padx=5)
        hand_labels.append(lbl)

    # ---- Next Card ----
    next_title = tk.Label(root, text="Next Card",
                          font=("Arial", 12, "bold"),
                          fg="white", bg="black")
    next_title.pack(pady=5)

    next_card_label = tk.Label(root, image=card_images["qmark"], bg="black")
    next_card_label.image = card_images["qmark"]
    next_card_label.pack()

    # ---- Update Loop ----
    def update_display():
        current_elixir = int(shared_state.get("opp_elixir", 0))
        current_hand = shared_state.get("curr_hand", [" ", " ", " ", " "])
        next_cards = shared_state.get("next_cards", [" "])
        next_card = next_cards[0] if len(next_cards) > 0 else " "

        # elixir bar
        elixir_canvas.delete("all")
        for i in range(10):
            x0 = i * 28
            color = "purple" if i < current_elixir else "gray"
            elixir_canvas.create_rectangle(
                x0, 0, x0+25, 20, fill=color, width=0
            )

        # current hand images
        for i, lbl in enumerate(hand_labels):
            name = current_hand[i] if i < len(current_hand) else " "
            img = card_images.get(name) or card_images["qmark"]
            lbl.config(image=img)
            lbl.image = img

        # next card
        nxt_img = card_images.get(next_card) or card_images["qmark"]
        next_card_label.config(image=nxt_img)
        next_card_label.image = nxt_img

        root.after(200, update_display)

    update_display()
    root.mainloop()


# ---- Main program ----
if __name__ == "__main__":
    q = Queue()
    manager = Manager()
    shared_state = manager.dict()

    shared_state["opp_elixir"] = 10
    shared_state["curr_hand"] = [" ", " ", " ", " "]
    shared_state["next_cards"] = [" "]

    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, "images")

    card_names = [
        "minipekka", "fireball", "musk", "giant",
        "minions", "knight", "archers", "goblins"
    ]

    # Start background processes
    p1 = Process(target=writer, args=(q, shared_state))
    p2 = Process(target=reader, args=(q, shared_state))
    p1.start()
    p2.start()

    run_gui(shared_state, images_dir, card_names)

    p1.terminate()
    p2.terminate()
