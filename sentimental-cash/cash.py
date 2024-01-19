from cs50 import get_float

# Get amount of change owed from the user
change_owed = get_float("Change Owed: ")
while change_owed <= 0:
    change_owed = get_float("Change Owed: ")

# Set number of coint to 0
num_coins = 0
change_owed_num = change_owed * 100

# Calculate number of coins owed
while change_owed_num > 0:
    if change_owed_num >= 25:
        change_owed_num -= 25
        num_coins += 1
    elif change_owed_num >= 10:
        change_owed_num -= 10
        num_coins += 1
    elif change_owed_num >= 5:
        change_owed_num -= 5
        num_coins += 1
    else:
        change_owed_num -= 1
        num_coins += 1

# Print number of coins for change owed
print(num_coins)
