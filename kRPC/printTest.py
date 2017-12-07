import sys, time

count = 0
while count < 40:
    # print(count, end="", flush=True)
    sys.stdout.write("\r" + str(count))
    sys.stdout.flush()
    time.sleep(.1)
    # print("\r")

    count += 1

# sys.stdout.write("hello")
# time.sleep(3)
#sys.stdout.write("bitch")
