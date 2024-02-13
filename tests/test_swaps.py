import asyncio
import json
from pprint import pprint

import websockets

from utils.constants import URI


async def listen_to_websocket():
    data = {
        "id": "1",
        "jsonrpc": "2.0",
        "method": "lp_subscribe_order_fills",
        "params": []
    }

    async with websockets.connect(URI) as websocket:
        await websocket.send(json.dumps(data))
        await websocket.recv()

        try:
            while True:
                resp = await websocket.recv()
                resp = json.loads(resp)
                pprint(resp)

        except websockets.ConnectionClosed as e:
            pprint(f'Connection closed')

        except Exception as e:
            pprint(f'An unknown error occurred {e}')


async def main():
    await listen_to_websocket()


if __name__ == '__main__':
    asyncio.run(main())