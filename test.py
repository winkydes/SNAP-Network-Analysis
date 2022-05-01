import random

count = 0

for i in range(100):
    if random.uniform(0,1) < 0.4:
        count = count + 1

print(count)
