import asyncio
import unittest

from src.order_book import OrderBook


class TestGetPrice(unittest.TestCase):
    def test_open_orders(self):
        async def async_test():
            order_book = OrderBook(base_asset='ETH', quote_asset="USDC") 
            await order_book.update()
            open_orders = order_book._get_open_orders()
            self.assertEqual(len(open_orders), 0)
        
        asyncio.run(async_test())

    def test_orderbook_liquidity_not_zero(self):
        async def async_test():
            order_book = OrderBook(base_asset='ETH', quote_asset="USDC")
            await order_book.update()  # Assuming this method populates bids and asks

            # Use the method to get total liquidity
            total_liquidity = order_book._get_total_liquidity()
            print('Total liquidity:', total_liquidity)
            self.assertNotEqual(total_liquidity, 0, "Total liquidity should not be 0")
        asyncio.run(async_test())

if __name__ == "__main__":
    unittest.main()
