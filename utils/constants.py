from enum import Enum

URI="ws://localhost:9944"

DECIMALS = {
    'USDC': 10 ** 6,
    'ETH': 10 ** 18,
    'BTC': 10 ** 8,
    'DOT': 10 ** 10,
    'FLIP': 10 ** 18
}

BASE_PRECISION = 18
QUOTE_PRECISION = 6

ASSET_1 = "ETH"
ASSET_2 = "USDC"
ASSET_3 = "BTC"
ASSET_4 = "USDT"

TICK_SIZE = 2

class Side(Enum):
    BUY="bid"
    SELL="ask"
    NONE="none"