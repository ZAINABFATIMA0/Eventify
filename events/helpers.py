import random
from datetime import datetime, timedelta

def generate_otp_and_expiry():
    otp = random.randint(100000, 999999)
    otp_expiry = datetime.now() + timedelta(minutes=5)
    return otp, otp_expiry
