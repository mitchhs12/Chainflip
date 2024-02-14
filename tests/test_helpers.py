import unittest

from utils.helpers import *


class TestGetPrice(unittest.TestCase):
    def test_hex_price (self):
        self.assertAlmostEqual(hex_price_to_decimal("0x44b82fa09b5a53ffffffd38ad","ETH", "USDC"), 1000.00)

    def test_price_to_hex (self):
        hex = decimal_to_hex_price(1000.00, "ETH", "USDC")
        self.assertAlmostEqual(hex_price_to_decimal(hex, "ETH", "USDC"), 1000.00)

    def test_tick_to_price(self):
        tick = 100
        expected_price = 1.0001 ** tick * (DECIMALS["ETH"] / DECIMALS["USDC"])
        result = tick_to_price(tick, "ETH", "USDC")
        self.assertAlmostEqual(result, expected_price, places=5, msg="tick_to_price does not match expected result.")

    def test_hex_amount_to_decimal(self):
        hex_string = "0x1BC16D674EC80000"  # Equals 2*10^18 in hex
        expected_amount = 2.0  # Assuming the asset is ETH with 10^18 decimals
        result = hex_amount_to_decimal(hex_string, "ETH")
        self.assertAlmostEqual(result, expected_amount, places=5, msg="hex_amount_to_decimal does not match expected result.")


if __name__ == "__main__":
    unittest.main()