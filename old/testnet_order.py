# from binance.client import Client
# Client.create_test_order()
from binance.exceptions import BinanceAPIException
from binance import AsyncClient
api_key = 'Q4AIVXYmXksBy9pG5JQUShsycrM0dfxmebuEcrJD4Jr1lvi1w9bYY2e7409pUC3U'
api_secret = 'FKUHuyR48b74V8mSjjTzVebXuTRLuTRQ6kFtK4m5zFhuTIWZKdCf5RFtMPLBjFlv'
from binance.helpers import round_step_size
    # update main
async def main():
    quantity = 0.001
    profit_pct = 1 + (3 / 100)
    purchase_price = 58802.609
    target_price = round_step_size(purchase_price * profit_pct, 0.01)
    print(f'target_price: {target_price}')
    client = await AsyncClient.create(api_key=api_key, api_secret=api_secret, testnet=True)
    try:
        limit_res = await client.order_limit_sell(symbol='BTCUSDT', price=target_price, quantity=quantity)
    except BinanceAPIException as e:
        print(e)
    else:
        print(json.dumps(limit_res, indent=2))
    await client.close_connection()