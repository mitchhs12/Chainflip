from src.chainflip import Chainflip
from utils.constants import Side
from utils.helpers import hex_amount_to_decimal, tick_to_price
from utils.types import LimitOrder, RangeOrder


class OrderBook(object):

    def __init__(self, base_asset: str, quote_asset:str, lp = None):
        self._chainflip = Chainflip()
        self._lp = lp
        self._base_asset = base_asset
        self._quote_asset = quote_asset
        self._bids = list()
        self._asks = list()
        self._range_orders = list()
        self._response = None
        self._open_orders = list()

    def _visualize_order_book(self):
        print(f"Order Book for {self._base_asset}/{self._quote_asset}")
        print("Bids:")
        
        for bid in self._bids:
            print(f"Price: {bid.price}, Quantity: {bid.quantity}, ID: {bid.id}")
        
        print("Asks:")
        for ask in self._asks:
            print(f"Price: {ask.price}, Quantity: {ask.quantity}, ID: {ask.id}")
    
    def _get_open_orders(self):
        return self._open_orders

    def _update_orderbook(self, data: dict):
        bids = list()
        asks = list()

        for bid in data['limit_orders']['bids']:
            price = tick_to_price(bid['tick'], self._base_asset)
            amount = hex_amount_to_decimal(bid['sell_amount'], self._quote_asset) / price
            if amount == 0:
                continue
            else:
                limit_buy = LimitOrder(
                    quantity=amount,
                    price=tick_to_price(bid['tick'], self._base_asset),
                    base_asset=self._base_asset,
                    quote_asset=self._quote_asset,
                    id=bid['id'],
                    side=Side.BUY,
                    lp_account=bid['lp']
                )
                bids.append(limit_buy)
                if limit_buy.lp_account == self._lp:
                    self._open_orders.append(limit_buy)

        for ask in data['limit_orders']['asks']:
            price = tick_to_price(ask['tick'], self._base_asset)
            amount = hex_amount_to_decimal(ask['sell_amount'], self._base_asset)
            if amount == 0:
                continue
            else:
                limit_sell = LimitOrder(
                    quantity=amount,
                    price=price,
                    base_asset=self._base_asset,
                    quote_asset=self._quote_asset,
                    id=ask['id'],
                    side=Side.SELL,
                    lp_account=ask['lp']
                )
                asks.append(limit_sell)
                if limit_sell.lp_account == self._lp:
                    self._open_orders.append(limit_sell)

        for range_order in data['range_orders']:
            range = RangeOrder(
                lower_price=tick_to_price(range_order['range']['start'], self._base_asset),
                upper_price=tick_to_price(range_order['range']['end'], self._base_asset),
                base_asset=self._base_asset,
                quote_asset=self._quote_asset,
                id=range_order['id'],
                quantity=range_order["liquidity"],
                lp_account=range_order['lp']
            )
            self._range_orders.append(range)
            if range.lp_account == self._lp:
                self._open_orders.append(range)

        self._bids = sorted(bids, key=lambda x: x.price, reverse=True)
        self._asks = sorted(asks, key=lambda x: x.price)

        try:
            self.top_bid = self._bids[0]
        except IndexError:
            print("No limit order bids in current order book")

        try:
            self._top_ask = self._asks[0]
        except IndexError:
            print("No limit order asks in current order book")

    async def update_orderbook(self):
        try:
            self.response = await self._chainflip(self._base_asset, self._quote_asset)
            self._update_orderbook(data=self.response['result'])
        except Exception as e:
            print(f"Error updating orderbook: {e}")
            raise e
        
    async def update(self):
        await self.update_orderbook()