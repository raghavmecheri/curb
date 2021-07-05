# Not empty script to test RAM overflow

from time import sleep

ctr = 0

arr = []

while True:
    print("Hello World!")
    arr += [bytearray(1024 * 1024 * 500)]
    ctr += 1
    sleep(5)
    if ctr == 50:
        break
