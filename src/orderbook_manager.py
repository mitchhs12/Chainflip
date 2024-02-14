from utils.types import LimitOrder, RangeOrder


class OrderManager(object):
    def __init__(self):
        self._limit_orders = dict()
        self._range_orders = dict()

    def get_limit_orders(self):
        return self._limit_orders
    
    def get_range_orders(self):
        return self._range_orders
    
    def add_limit_order(self, order: LimitOrder):
        self._limit_orders[order.id] = order

    def add_range_order(self, order: RangeOrder):
        self._range_orders[order.id] = order

    def remove_limit_order(self, order: LimitOrder):
        del self._limit_orders[order.id]
    
    def remove_range_order(self, order: RangeOrder):
        del self._range_orders[order.id]

