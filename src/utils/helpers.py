from decimal import Decimal, getcontext

from utils.constants import DECIMALS

# Set a high precision to handle the calculations
getcontext().prec = 50

def hex_price_to_decimal(u256_hex_str: str, asset_1: str, asset_2: str) -> float:
    # Convert hex string to integer
    u256_integer = int(u256_hex_str, 16)

    # Extract the integer part (the top 128 bits) & convert integer part to float
    float_integer = float(u256_integer >> 128)

    # Extract the fractional part (the bottom 128 bits) & convert fractional part to its decimal equivalent
    float_fractional = float(u256_integer & ((1 << 128) - 1)) / (1 << 128)

    # Combine and return the result
    return (float_integer + float_fractional) * (DECIMALS[asset_1] / DECIMALS[asset_2])


def decimal_to_hex_price(price: float, asset_1: str, asset_2: str) -> str:
    # Convert price to Decimal for high precision arithmetic
    price_decimal = Decimal(price)

    # Adjust the price by the precision factors of the assets
    adjusted_price = price_decimal * Decimal(DECIMALS[asset_2]) / Decimal(DECIMALS[asset_1])

    # Scale the adjusted price to the 128-bit fractional part of the fixed-point format
    fractional_part = (adjusted_price - int(adjusted_price)) * (Decimal(2) ** Decimal(128))

    # Construct the 256-bit integer
    u256_integer = (int(adjusted_price) << 128) + int(fractional_part)

    # Convert to hexadecimal string
    u256_hex_str = hex(u256_integer)

    return u256_hex_str


def hex_amount_to_decimal(hex_string: str, asset: str) -> float:
    return float(str((int(hex_string, 16)) / DECIMALS[asset]))

def tick_to_price(tick: int, asset_1: str, asset_2: str = 'USDC') -> float:
    price = 1.0001 ** tick
    return price * (DECIMALS[asset_1] / DECIMALS[asset_2])