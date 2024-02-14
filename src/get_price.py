import asyncio
import json
from pprint import pprint

import websockets

from utils.constants import *
from utils.helpers import hex_amount_to_decimal, hex_price_to_decimal


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
        response = await websocket.recv()
        
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
        response_data = json.loads(response)
        pprint(f"Pool Liquidity Response: {response_data}", compact=True)

        result = response_data.get("result", {})
        limit_orders = result.get("limit_orders", [])
        range_orders = result.get("range_orders", [])

        # Calculate total liquidity for limit orders (bids)
        total_limit_orders_bid_amounts = sum(hex_amount_to_decimal(bid["amount"], "USDC") for bid in limit_orders.get("bids", []))

        # Calculate total liquidity for range orders
        total_range_orders_liquidity = sum(hex_amount_to_decimal(order["liquidity"], "BTC") for order in range_orders)

        pprint(f"Total Liquidity for Limit Orders (Bids): {total_limit_orders_bid_amounts}", compact=True)
        pprint(f"Total Liquidity for Range Orders: {total_range_orders_liquidity}", compact=True)
        return {
            "total_limit_orders_bid_amounts": total_limit_orders_bid_amounts,
            "total_range_orders_liquidity": total_range_orders_liquidity
        }
            


# Run both coroutines concurrently
async def main():
    await asyncio.gather(
        subscribe_pool_price("ETH", "USDC"),
        get_pool_liquidity("BTC", "USDC")
    )

if __name__ == "__main__":
    asyncio.run(main())
