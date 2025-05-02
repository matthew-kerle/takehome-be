def convert_price_to_cents(price_str):
    """
    Convert price string like '$739K' or '$2.8M' to cents.
    
    Args:
        price_str (str): Price string in format like '$739K' or '$2.8M'
        
    Returns:
        int: Price in cents, or None if conversion fails
    """
    if not price_str:
        return None
        
    # Remove $ and any whitespace
    price_str = price_str.strip().replace('$', '').replace(',', '')
    
    # Check for K or M suffix
    multiplier = 1
    if price_str.endswith('K'):
        multiplier = 1000
        price_str = price_str[:-1]
    elif price_str.endswith('M'):
        multiplier = 1000000
        price_str = price_str[:-1]
        
    try:
        # Convert to float, multiply by multiplier, then convert to cents
        return int(float(price_str) * multiplier * 100)
    except (ValueError, TypeError):
        return None

def format_price_from_cents(price_cents):
    """
    Convert price in cents to a human-readable format.
    
    Args:
        price_cents (int): Price in cents
        
    Returns:
        str: Formatted price string with appropriate commas and/or M suffix for values over $10M
    """
    if not price_cents:
        return None
        
    dollars = price_cents / 100
    
    if dollars >= 10000000:  # $10M+
        return f"${dollars/1000000:.1f}M"
    else:
        return f"${dollars:,.0f}" 