import asyncio,json
from binance.exceptions import BinanceAPIException
from binance import AsyncClient
    # update main

async def limit_buy(api_key,api_secret,cc,minNotional,nbbo_plusOne):
    client = await AsyncClient.create(api_key=api_key, api_secret=api_secret)
    try:
        limit_buy_response = await client.order_limit_buy(symbol=cc, quantity=round(minNotional/nbbo_plusOne,4),price=nbbo_plusOne)
        client.spot
    except BinanceAPIException as e:
        print(e)
    # else:
    #     print(json.dumps(limit_buy_response, indent=2))
    await client.close_connection()
    return limit_buy_response

async def oco_sell(api_key,api_secret,cc,minNotional,LastPrice,lastAsk_minusOne,lastBid_plusOne,stopLoss_percent):
    client = await AsyncClient.create(api_key=api_key, api_secret=api_secret)
    try:
        oco_sell_response = await client.create_oco_order(
            symbol=cc,
            side='SELL',
            stopLimitTimeInForce = 'GTC',
            quantity=round(minNotional/LastPrice,4),
            price=lastAsk_minusOne,
            stopPrice=lastBid_plusOne*stopLoss_percent)
    except BinanceAPIException as e:
        print(e)
    # else:
    #     print(json.dumps(limit_sell_response, indent=2))
    await client.close_connection()
    return oco_sell_response

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
    