
import random

# Generate a random integer between 0 and 0xFFFFF (inclusive)
# 0xFFFFF is the largest 5-digit hexadecimal number, which is 1048575 in decimal.
random_int = random.randint(0, 0xFFFFF)

# Format the integer as a 5-digit uppercase hexadecimal string,
# padding with leading zeros if necessary.
hex_number = "{:05X}".format(random_int)

print(f"Random 5-digit hexadecimal number: {hex_number}")
