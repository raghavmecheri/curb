# Empty (ish) script to test exec

from time import sleep

ctr = 0

while True:
    print("Hello World!")
    ctr += 1
    sleep(5)
    if ctr == 50:
        break
