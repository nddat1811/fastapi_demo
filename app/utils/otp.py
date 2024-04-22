import random

# Generate random 6 digits to create otp
def generate_otp():
    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    return otp
