from asyncio import as_completed
from game import Trace, connect_agent, Game, Board
import pickle
from queue import Queue
from threading import Thread
import threading
import concurrent.futures

enclosure_queue = Queue()
lock = threading.Lock()

def save_trace():
    while True:
        trace: Trace = enclosure_queue.get()
        lock.acquire()
        with open('assets/greedy.pkl', 'ab') as f:
            pickle.dump(trace, f)
        lock.release()
        enclosure_queue.task_done()

def play():
    agents = ['http://localhost:8000', 'http://localhost:8000']
    credits = [None, None]
    board = Board()

    for i in range(2):
        agents[i] = connect_agent(agents[i])

    game = Game(agents, board, None, credits)
    game.startPlaying()

    # Once game is done, push trade to queue
    enclosure_queue.put(game.trace)

def main():
    # Start thread to save trace
    t = Thread(target=save_trace)
    t.daemon = True
    t.start()

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_num = { executor.submit(play): i for i in range(1_000_000)}
        for future in concurrent.futures.as_completed(future_to_num):
            id = future_to_num[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (id, exc))
            else:
                print(f"Game {id} done")

    # Wait for queue to be empty
    enclosure_queue.join()

if __name__ == '__main__':
    main()