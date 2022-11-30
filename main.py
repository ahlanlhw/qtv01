import asyncio,json
from all_tickers import tradable_tickers
from id import id
from order_manager import limit_buy,oco_sell,qry_open_order_status,market_sell_order
from acc_bal import login
bal = login()
top_3 = bal[~bal['asset'].str.contains('LD')][['asset','free']].sort_values(by='free',ascending=False).set_index('asset').iloc[:3]
usdt_avail =top_3.loc['USDT']['free']
api_key,secret_key = id()
### calls method and saves all exchange_info on the same folder to prepare for calculation
tradable_tickers = tradable_tickers(api_key,secret_key)
### method to get the 20 most liquid 
### return pairs here retrieved from tradestream data
cc = 'ETHUSDT'
### update minimum trade amount to
minNotional=10
LastPrice=2
### function tuples here
### add the list of tasks that you wnat to perform here.
market_sell_task = market_sell_order(api_key,secret_key,cc,minNotional,LastPrice)
open_orders_task =qry_open_order_status(api_key,secret_key,cc)

if __name__ == "__main__":
    print(f'Starting Portfolio Value is {usdt_avail}')
    # loop = asyncio.get_event_loop()
    ### queried all the exchange guidelines to follow
    # sym_details,exch = loop.run_until_complete(asyncio.gather(*tasks))
    ### did a market sell here
    # market_sell_response = loop.run_until_complete(market_sell_task)
    # market_sell_response returns as dictionary object, we can save all our transactions into csv.
    # if market_sell_response: read_trade_csv, if not create, need to have a trade dictionary,
    # trade.update(market_sell_response), pd.DataFrame.from_dict(trade).reset_index(drop=true).to_csv(index=False)
    
    ### queries all open orders
    # open_order_status = loop.run_until_complete(open_orders_task)
    # open_order_status = asyncio.run(open_orders_task)
    # if open_order_status:
    #     print(f'You currently have {len(open_order_status)} for {cc}')
    # loop.close()
import pandas as pd
exch_sym = pd.json_normalize(exch['symbols'])
exch_sym['permissions'] = exch_sym['permissions'].str.join(', ')
spot_mgn_pairs = exch_sym[(exch_sym['permissions'].str.contains('SPOT, MARGIN')) & (exch_sym['quoteAsset']=='USDT')]
# spot_mgn_pairs = exch_sym[(exch_sym['permissions'].str.contains('SPOT, MARGIN')) & (exch_sym['quoteAsset'].str.contains('|'.join(['USD','EUR','GBP']))==False)]
# spot_mgn_pairs[spot_mgn_pairs['symbol']=='BTCUSDT']['filters'].iloc[-1]
### get min tickSize, minQty,maxQty, maxNumOrders
df = pd.DataFrame()
for k,v in spot_mgn_pairs.iterrows():
    print(v['symbol'])
    for kk in "tickSize, minQty, maxQty, maxNumOrders, minNotional".split(", "):
        if kk !='maxQty':
            v[kk] = pd.DataFrame(v['filters']).set_index('filterType')[kk].dropna().max()
        else:
            v[kk] = pd.DataFrame(v['filters']).set_index('filterType')[kk].astype('float').dropna()['MARKET_LOT_SIZE']
        print(f"{v['symbol']}'s {kk} is {v[kk]}")
    df = pd.concat([df,pd.DataFrame(v).T],axis=0)
# df['quoteAsset'].drop_duplicates()
df[df['baseAsset']=='ETH'].iloc[-1]['filters']
df[df['baseAsset']=='ETH'].iloc[-1]
round(10/3500,4)
# df[['quotePrecision', 'quoteAssetPrecision', 'baseCommissionPrecision',
#        'quoteCommissionPrecision']].drop_duplicates() 