import random

# Generate random 6 digits to create code
def generate_code():
    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    return otp
