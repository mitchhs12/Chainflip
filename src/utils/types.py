from dataclasses import dataclass

from utils.constants import Side


@dataclass
class LimitOrder:
    lp_account: str
    base_asset: str
    quote_asset: str
    side: Side
    id: str # actually a hexadecimal
    price: float
    quantity: float

@dataclass
class RangeOrder:
    lp_account: str
    base_asset: str
    quote_asset: str
    id: str # actually a hexadecimal
    lower_price: float
    upper_price: float
    quantity: float
   