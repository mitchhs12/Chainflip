class LimitOrder:
    amount: float
    price:float
    base: str
    quote: str

class RangeOrder:
    lower_bound: float
    upper_bound: float
    base: str
    quote: str
    