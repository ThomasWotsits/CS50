from cs50 import get_int

# Asking for height between 1 and 8
height = get_int("Height: ")
while height < 1 or height > 8:
    print("Input a interger between 1 and 8")
    height = get_int("Height: ")

# Block building loop
for i in range(1, height + 1):
    print(" " * (height - i) + "#" * i)
