import time

frame_cap = 1.0/60
time_1 = time.perf_counter()
unprocessed = 0
t = 10
tex = 0
while t >= 0:
    time_2 = time.perf_counter()
    passed = time_2 - time_1
    t -= passed
    unprocessed += passed
    time_1 = time_2
    while(unprocessed >= frame_cap):
        for i in range(100000):
            x= i
        tex+=1
        unprocessed-=frame_cap
    
        # put everything inside here
