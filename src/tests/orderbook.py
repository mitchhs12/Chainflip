import asyncio
import json
from pprint import pprint

import websockets

from utils.constants import *


async def listen_to_websocket():
    data = {
        "id": "1",
        "jsonrpc": "2.0",
        "method": "cf_pool_orderbook",
        "params": {"base_asset": "ETH", "quote_asset": "USDC", "orders": 10}
    }

    async with websockets.connect(URI) as websocket:
        await websocket.send(json.dumps(data))
        response = await websocket.recv()
        pprint(f'Response: {response}')

        try:
            while True:
                resp = await websocket.recv()
                resp = json.loads(resp)
                pprint(resp)

        except websockets.ConnectionClosed as e:
            pprint(f'Connection closed with error: {e}')

        except Exception as e:
            pprint(f'An unknown error occurred: {e}')


async def main():
    await listen_to_websocket()


if __name__ == '__main__':
    asyncio.run(main())