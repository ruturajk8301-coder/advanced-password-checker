import re
import math
import string


def calculate_entropy(password):
    """
    Calculates a penalized password entropy estimate based on
    character diversity, length, and structural patterns.
    """

    if not password:
        checks = {
            "lower": False,
            "upper": False,
            "digit": False,
            "special": False,
            "length": False
        }
        return 0.0, checks

    # 1. Character category checks
    checks = {
        "lower": bool(re.search(r"[a-z]", password)),
        "upper": bool(re.search(r"[A-Z]", password)),
        "digit": bool(re.search(r"[0-9]", password)),
        "special": any(char in string.punctuation for char in password),
        "length": len(password) >= 8
    }

    # 2. Calculate character search-space size
    pool_size = 0

    if checks["lower"]:
        pool_size += len(string.ascii_lowercase)

    if checks["upper"]:
        pool_size += len(string.ascii_uppercase)

    if checks["digit"]:
        pool_size += len(string.digits)

    if checks["special"]:
        pool_size += len(string.punctuation)

    if pool_size == 0:
        return 0.0, checks

    # 3. Base search-space entropy estimate
    entropy = len(password) * math.log2(pool_size)

    # 4. Pattern penalty deductions
    penalties = 0.0

    # Penalty for common password-style starting patterns
    if re.match(r"^[A-Z][a-z]{3,}", password):
        penalties += 12.0

    # Penalty for trailing sequential numbers
    if re.search(r"\d{3,3}$", password) or "1234" in password:
        penalties += 15.0

    # Penalty for repeated characters
    repeated_chars = len(password) - len(set(password))
    penalties += repeated_chars * 2.5

    # Apply deductions without allowing negative entropy
    final_entropy = max(0.0, round(entropy - penalties, 2))

    return final_entropy, checks
