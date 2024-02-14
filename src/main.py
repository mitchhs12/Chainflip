import asyncio
import json
from pprint import pprint

import websockets

from src.order_book import OrderBook
from utils.constants import *
from utils.helpers import hex_price_to_decimal


async def subscribe_pool_price(from_asset, to_asset):
    async with websockets.connect(URI) as websocket:
        # Subscribe to pool price
        subscribe_message = {
            "jsonrpc": "2.0",
            "method": "cf_subscribe_pool_price",
            "params": {
                "from_asset": from_asset,
                "to_asset": to_asset
            },
            "id": 1
        }
        await websocket.send(json.dumps(subscribe_message))
        
        # Listen for messages
        async for message in websocket:
            response = json.loads(message)
            pprint(f"Pool Price Update: {response}", compact=True)

            # Process the message to extract and log the current price
            if 'method' in response and response['method'] == 'cf_subscribe_pool_price':
                current_price_info = response.get('params', {}).get('result', {})
                price = current_price_info.get('price')
                if price:
                    pprint(f"Formatted Current Price: {hex_price_to_decimal(price, ASSET_1, ASSET_2)}", compact=True)

async def get_pool_liquidity(base_asset, quote_asset):
    async with websockets.connect(URI) as websocket:
        liquidity_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "cf_pool_liquidity",
            "params": {
                "base_asset": base_asset,
                "quote_asset": quote_asset
            }
        }
        await websocket.send(json.dumps(liquidity_message))
        response = await websocket.recv()
        pprint(f"Pool Liquidity Response: {response}", compact=True)

# Run both coroutines concurrently
async def main():
    # await asyncio.gather(
    #     subscribe_pool_price("ETH", "USDC"),
    #     get_pool_liquidity("BTC", "USDC")
    # )
    order_book = OrderBook(base_asset='ETH', quote_asset="USDC")  # Example for Ethereum

    await order_book.update()

    order_book._visualize_order_book()

    print('open orders', order_book._get_open_orders())


if __name__ == "__main__":
    asyncio.run(main())
