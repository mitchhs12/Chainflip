import asyncio

from src.order_book import OrderBook


# Run both coroutines concurrently
async def main():
    order_book = OrderBook(base_asset='ETH', quote_asset="USDC")  # Example for Ethereum

    await order_book.update()

    order_book._visualize_order_book()

    print('open orders', order_book._get_open_orders())


if __name__ == "__main__":
    asyncio.run(main())
