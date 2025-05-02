def convert_price_to_cents(price_str):
    """
    Convert price string like '$739K' or '$2.8M' to cents.
    Also handles numeric inputs that are already in cents.

    Args:
        price_str (str or int or float): Price in format like '$739K' or '$2.8M',
            or numeric value in cents

    Returns:
        int: Price in cents, or None if conversion fails
    """
    if price_str is None:
        return None

    # If it's already a number, assume it's in cents
    if isinstance(price_str, (int, float)):
        return int(price_str)

    # Remove $ and any whitespace
    price_str = str(price_str).strip().replace("$", "").replace(",", "")

    # Check for K or M suffix
    multiplier = 1
    if price_str.endswith("K"):
        multiplier = 1000
        price_str = price_str[:-1]
    elif price_str.endswith("M"):
        multiplier = 1000000
        price_str = price_str[:-1]

    try:
        # Convert to float, multiply by multiplier, then convert to cents
        return int(float(price_str) * multiplier * 100)
    except (ValueError, TypeError):
        return None


def format_price_from_cents(cents):
    """Convert integer cents to formatted price string."""
    if cents is None or cents == 0:
        return None

    # Round to nearest dollar
    dollars = round(cents / 100)

    # Use M suffix for amounts >= $10M, comma formatting for all other amounts
    if dollars >= 10_000_000:
        return f"${dollars/1_000_000:.1f}M"
    return f"${dollars:,}"


def parse_price_to_cents(price_str):
    """
    Convert a price string or float to cents.
    Handles formats like:
    - "2.5M" or "2.5m" -> 250000000 (cents)
    - "750K" or "750k" -> 75000000 (cents)
    - "1500.50" -> 150050 (cents)
    - 2500000.50 -> 250000050 (cents)
    """
    if price_str is None:
        return None

    # If it's already a number, convert to cents
    if isinstance(price_str, (int, float)):
        return int(price_str * 100)

    # Remove whitespace and $ signs
    price_str = price_str.strip().replace("$", "").replace(",", "")

    try:
        # Handle M/m suffix (millions)
        if price_str.lower().endswith("m"):
            value = float(price_str[:-1]) * 1_000_000 * 100
            return int(value)

        # Handle K/k suffix (thousands)
        if price_str.lower().endswith("k"):
            value = float(price_str[:-1]) * 1_000 * 100
            return int(value)

        # Handle plain numbers
        return int(float(price_str) * 100)
    except (ValueError, TypeError):
        return None


def convert_price_param_to_cents(param):
    """Convert a price parameter to cents, handling both string and float inputs."""
    if param is None:
        return None

    try:
        # If it's a string that might have K/M suffix
        if isinstance(param, str):
            return parse_price_to_cents(param)
        # If it's a number (float/int), convert to cents
        return int(float(param) * 100)
    except (ValueError, TypeError):
        return None


def safe_int(value):
    """Safely convert a value to int, returning None if conversion fails."""
    if value is None or (isinstance(value, str) and value.strip() == ""):
        return None
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return None
