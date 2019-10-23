from cs50 import get_float

while True:
    n = get_float("Change owed: ")
    if n > 0:
        break

n *= 100
coins = 0

while n >= 25:
    n -= 25
    coins += 1
while n >= 10:
    n -= 10
    coins += 1
while n >= 5:
    n -= 5
    coins += 1
print(f"{int(coins + n)}")
