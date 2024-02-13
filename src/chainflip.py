class Chainflip:
    """
    Main Chainflip Interface
    """
    def __init__(self):
        pass

    async def get_orders(self, base_asset, quote_asset):
        data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "cf_pool_orders",
            "params": {
                "base_asset": base_asset,
                "quote_asset": quote_asset
            }
        }