import asyncio,json
import pandas as pd
from binance import Client

def tradable_tickers(api_key,secret_key):
    client = Client(api_key,secret_key)
    exch = client.get_exchange_info()
    client.close_connection()
    exch_sym = pd.json_normalize(exch['symbols'])
    exch_sym['permissions'] = exch_sym['permissions'].str.join(', ')
    spot_mgn_pairs = exch_sym[(exch_sym['permissions'].str.contains('SPOT, MARGIN')) & (exch_sym['quoteAsset']=='USDT')]
    df = pd.DataFrame()
    for k,v in spot_mgn_pairs.iterrows():
        for kk in "tickSize, minQty, maxQty, maxNumOrders, minNotional".split(", "):
            if kk !='maxQty':
                v[kk] = pd.DataFrame(v['filters']).set_index('filterType')[kk].dropna().max()
            else:
                v[kk] = pd.DataFrame(v['filters']).set_index('filterType')[kk].astype('float').dropna()['MARKET_LOT_SIZE']
            # print(f"{v['symbol']}'s {kk} is {v[kk]}")
        df = pd.concat([df,pd.DataFrame(v).T],axis=0)
    df.to_csv('tradable_tickers.csv',index=False)
    return df
if __name__ == "__main__":
    tradable_tickers()
    
