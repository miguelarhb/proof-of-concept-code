import timeit
from time import sleep

def start():
    global start
    start = timeit.default_timer()

def end():
    global start
    stop = timeit.default_timer()
    result = stop - start
    return result

def delay(event):
    print("INFO: Sleeping after " + event + "..." , end =" ")
    sleep(1)
    print("Waking Up!")