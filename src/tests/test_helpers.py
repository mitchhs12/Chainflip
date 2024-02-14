import unittest

from utils.helpers import *


class TestGetPrice(unittest.TestCase):
    def test_hex_price (self):
        self.assertAlmostEqual(hex_price_to_decimal("0x44b82fa09b5a53ffffffd38ad","ETH", "USDC"), 1000.00)

    def test_price_to_hex (self):
        hex = decimal_to_hex_price(1000.00, "ETH", "USDC")
        self.assertAlmostEqual(hex_price_to_decimal(hex, "ETH", "USDC"), 1000.00)

    def test_tick_to_price (self):
        # TODO: Implement this test
        pass

if __name__ == "__main__":
    unittest.main()