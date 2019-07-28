import time
import sys
i = 0
while True:
    print("Now %s"%i)
    sys.stdout.flush()
    time.sleep(2)
    i += 1
