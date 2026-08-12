import re
import math

def calculate_entropy(password):
    """
    Calculates a penalized entropy score based on character diversity,
    length requirements, and structural patterns.
    """
    if not password:
        checks = {"lower": False, "upper": False, "digit": False, "special": False, "length": False}
        return 0.0, checks

    # 1. Base lookups
    checks = {
        "lower": bool(re.search(r"[a-z]", password)),
        "upper": bool(re.search(r"[A-Z]", password)),
        "digit": bool(re.search(r"[0-9]", password)),
        "special": bool(re.search(r"[!@#$%^&*()_+=\-`~[\]{}|;:',.<>/? ]", password)),
        "length": len(password) >= 8  # New Length Validation Check
    }

    # 2. Character search space pool calculation
    pool_size = 0
    if checks["lower"]: pool_size += 26
    if checks["upper"]: pool_size += 26
    if checks["digit"]: pool_size += 10
    if checks["special"]: pool_size += 32

    if pool_size == 0:
        return 0.0, checks

    # 3. Base Shannon Entropy
    entropy = len(password) * math.log2(pool_size)

    # 4. Pattern Penalty Deductions (De-masking human habits)
    penalties = 0.0

    # Penalty for common dictionary starting patterns (e.g., 'Password...')
    if re.match(r"^[A-Z][a-z]{3,}", password):
        penalties += 12.0

    # Penalty for trailing sequential numbers (e.g., '1234')
    if re.search(r"\d{3,3}$", password) or "1234" in password:
        penalties += 15.0

    # Penalty for repetitive characters (e.g., 'aaaa')
    repeated_chars = len(password) - len(set(password))
    penalties += (repeated_chars * 2.5)

    # Apply deductions safely without dropping below 0
    final_entropy = max(0.0, round(entropy - penalties, 2))

    return final_entropy, checks

