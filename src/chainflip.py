import aiohttp

from utils.constants import URI


class Chainflip(object):
    def __init__(self):
        self._client = aiohttp.ClientSession
        self._orders = self.get_orders
    
    async def await_response(self, header: dict, data: dict):
        async with self._client(headers=header) as session:
            async with session.post(url=URI, json=data) as response:
                self._response = await response.json()

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
        await self.await_response({'Content-Type': 'application/json'}, data)

    async def __call__(self, *args):
        await self.get_orders(*args)
        return self._response