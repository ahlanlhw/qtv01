import asyncio,json
from binance.exceptions import BinanceAPIException
from binance import AsyncClient

async def qry_open_order_status(api_key,api_secret,cc):
    client = await AsyncClient.create(api_key=api_key, api_secret=api_secret)
    try:
        open_order_status = await client.get_open_orders(symbol=cc)
    except BinanceAPIException as e:
        print(e)
    # else:
    #     print(json.dumps(open_order_status, indent=2))
    await client.close_connection()
    return open_order_status

# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(qry_open_order_status(api_key,api_secret,cc))
