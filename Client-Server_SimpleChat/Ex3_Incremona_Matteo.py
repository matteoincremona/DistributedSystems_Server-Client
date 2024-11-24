import threading
import random
import time

def thr(id):
    print(f"Hi, I'm thread {id}") # Greeting the user
    sleep_t = random.uniform(1, 5) # Because not specified, I chose these values as min and max sleep time
    time.sleep(sleep_t)
    print(f"Goodbye from thread {id}") # Farewell message

for i in range(3):
    thread = threading.Thread(target = thr, args =(i,))
    thread.start()

