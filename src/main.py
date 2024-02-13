import asyncio
import json

import websockets

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
            print(f"Pool Price Update: {response}")

            # Process the message to extract and log the current price
            if 'method' in response and response['method'] == 'cf_subscribe_pool_price':
                current_price_info = response.get('params', {}).get('result', {})
                price = current_price_info.get('price')
                if price:
                    print(f"Formatted Current Price: {hex_price_to_decimal(price, ASSET_1, ASSET_2)}")

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
        print(f"Pool Liquidity Response: {response}")

# Run both coroutines concurrently
async def main():
    await asyncio.gather(
        subscribe_pool_price("ETH", "USDC"),
        get_pool_liquidity("BTC", "USDC")
    )

asyncio.run(main())