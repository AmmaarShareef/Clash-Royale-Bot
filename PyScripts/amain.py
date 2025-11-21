#amain.py

from multiprocessing import Process, Queue
from card_det import writer
from elix_deck import reader

if __name__ == "__main__":
    q = Queue()
    
    p1 = Process(target=writer, args=(q,))
    p2 = Process(target=reader, args=(q,))
    
    try:
        p1.start()
        p2.start()
        p1.join()
        p2.join()
    except KeyboardInterrupt:
        p1.terminate()
        p2.terminate()