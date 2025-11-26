#amain.py

from multiprocessing import Process, Queue, Manager
from card_det import writer
from elix_deck import reader
import tkinter as tk

# ---- GUI function ----
def run_gui(shared_state, card_images):
    root = tk.Tk()
    root.title("Clash Royale Helper Display")
    root.geometry("400x250")  # a bit taller for titles

    # Canvas for elixir
    elixir_canvas = tk.Canvas(root, width=300, height=20)
    elixir_canvas.pack(pady=5)

    # ---- TITLE: Current Hand ----
    hand_title = tk.Label(root, text="Current Hand", font=("Arial", 12, "bold"))
    hand_title.pack()

    # Frame for hand cards
    hand_frame = tk.Frame(root)
    hand_frame.pack(pady=5)
    hand_labels = [tk.Label(hand_frame, text="") for _ in range(4)]
    for lbl in hand_labels:
        lbl.pack(side=tk.LEFT, padx=5)

    # ---- TITLE: Next Card ----
    next_title = tk.Label(root, text="Next Card", font=("Arial", 12, "bold"))
    next_title.pack(pady=5)

    # Label for the next card image/text
    next_card_label = tk.Label(root, text="")
    next_card_label.pack()

    # Update loop
    def update_display():
        # Fetch current state
        current_elixir = int(shared_state.get("opp_elixir", 0))
        current_hand = shared_state.get("curr_hand", [" ", " ", " ", " "])
        next_cards = shared_state.get("next_cards", [" ", " ", " ", " "])
        next_card = next_cards[0] if len(next_cards) > 0 else " "

        # Draw elixir as purple squares
        elixir_canvas.delete("all")
        for i in range(10):
            x0 = i * 28
            color = "purple" if i < current_elixir else "gray"
            elixir_canvas.create_rectangle(x0, 0, x0+25, 20, fill=color)

        # Update hand card labels
        for i, lbl in enumerate(hand_labels):
            card_name = current_hand[i] if i < len(current_hand) else " "
            img = card_images.get(card_name)
            if img:
                lbl.config(image=img, text="")
                lbl.image = img  # keep a reference
            else:
                lbl.config(text=card_name, image="")

        # Update next card label
        img_next = card_images.get(next_card)
        if img_next:
            next_card_label.config(image=img_next, text="")
            next_card_label.image = img_next
        else:
            next_card_label.config(text=next_card, image="")

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
    shared_state["next_cards"] = [" ", " ", " ", " "]

    card_names = ["minipekka", "fireball", "musk", "giant", "minions", "knight", "archers", "goblins"]
    card_images = {}
    for name in card_names:
        try:
            card_images[name] = tk.PhotoImage(file=f"images/{name}.png")
        except Exception:
            card_images[name] = None

    p1 = Process(target=writer, args=(q, shared_state))
    p2 = Process(target=reader, args=(q, shared_state))
    p1.start()
    p2.start()

    run_gui(shared_state, card_images)

    p1.terminate()
    p2.terminate()
