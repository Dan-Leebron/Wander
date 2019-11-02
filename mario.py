from cs50 import get_int
# making sure the number entered is within the range we want
while True:
    n = get_int("Height: ")
    if n >= 1 and n <= 8:
        break
# printing the appropriate number of spaces and hashes per row
for i in range(n):
    print(" " * (n - i - 1), end="")
    print("#" * (i + 1))

