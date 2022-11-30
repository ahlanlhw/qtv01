import asyncio,json
from binance.exceptions import BinanceAPIException
from binance import AsyncClient
# from binance.client import Client
# Client.create_test_order()
    # update main
async def market_sell_order(api_key,api_secret,cc,minNotional,LastPrice):
    client = await AsyncClient.create(api_key=api_key, api_secret=api_secret)
    try:
        market_sell_response = await client.order_market_sell(symbol=cc, quantity=round(minNotional/LastPrice,4))
    except BinanceAPIException as e:
        print(e)
    else:
        print(json.dumps(market_sell_response, indent=2))
    await client.close_connection()
    return market_sell_response
    

# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(market_sell_order(api_key,api_secret,cc,minNotional,LastPrice))
