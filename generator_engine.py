import secrets
import string


def generate_secure_password(length=16):
    """Generate a cryptographically secure random password."""

    if length < 4:
        raise ValueError("Password length must be at least 4.")

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*()_+"

    all_characters = lowercase + uppercase + digits + symbols

    # Guarantee at least one character from each required category
    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(symbols)
    ]

    # Fill the remaining positions using cryptographically secure randomness
    password += [
        secrets.choice(all_characters)
        for _ in range(length - 4)
    ]

    # Securely construct the final order without using random.shuffle()
    result = []

    while password:
        index = secrets.randbelow(len(password))
        result.append(password.pop(index))

    return "".join(result)