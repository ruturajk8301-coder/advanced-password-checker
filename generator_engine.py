import random
import string


def generate_secure_password(length=16):
    """Generates an extremely secure, random password string."""
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*()_+"

    all_characters = lowercase + uppercase + digits + symbols

    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(symbols)
    ]

    password += [random.choice(all_characters) for _ in range(length - 4)]

    random.shuffle(password)

    return "".join(password)
