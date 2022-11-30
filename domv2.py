import websockets,json,asyncio
import pandas as pd
import datetime
import printer

exec(open('printer.py').read())


### for multiple streams
# tolerance = input("What's the tolerance you want? tolerance = 0.02 is 2.00%")
ticker_list = ['ethusdt','ftmusdt','solusdt','btcusdt','celrusdt','dydxusdt','avausdt','oneusdt']
interval = 1000
stream_type = f'@depth@{interval}ms'
request_string = [k+f'{stream_type}' for k in ticker_list]
request_string = '/'.join(request_string)
socket=f"wss://stream.binance.com:9443/stream?streams=" +request_string ###
msg = {
        "method": "SUBSCRIBE",
        "params":
        ticker_list,
        "id": 1
        }

def arrange_order_book(data):
    if "order_book" not in globals():
        global order_book
        order_book = pd.DataFrame()
    else:
        order_book = pd.concat([order_book,data],axis=0,ignore_index=True)
        order_book = order_book.sort_values(by=['symbol','price'],ascending=False).drop_duplicates(subset=data.columns.difference(['event_id','time','quantity','side']),keep='first')
        order_book = order_book[order_book['quantity']!=0]
        return order_book

async def do_something(response):
    global results,dd
    results = json.loads(response)
    ### cleans the data and organizes the orderbook
    ba = {side: pd.DataFrame(data=results['data'][side], columns=["price", "quantity"],dtype=float)for side in ["b", "a"]}
    ba_list = [ba[side].assign(side=side) for side in ba]
    data = pd.concat(ba_list, axis="index", ignore_index=True, sort=True)
    data['event_id'] = str(results['data']['u'])
    data['time'] = str(results['data']['E'])
    data['symbol'] = str(results['data']['s'])
    data = data[['event_id','time','price','quantity','side','symbol']]
    order_book = arrange_order_book(data)
    tolerance=0.006
    d = {}
    dd = {}
    for k in set(order_book['symbol']):
        # k = 'SOLUSDT'
        temp_df = order_book[order_book['symbol']==k].reset_index(drop=True)
        temp_df['EventTime'] = pd.to_datetime(temp_df['time'],unit='ms')
        mid_price = (temp_df[(temp_df['side']=='b')]['price'].max()+temp_df[(temp_df['side']=='a')]['price'].min())/2
        lb = temp_df[(temp_df['price']>mid_price*(1-tolerance)) & (temp_df['side']=='b')].sort_values(by=['quantity'],ascending=False).head(3)[['EventTime','price','quantity','symbol','side']]
        ub = temp_df[(temp_df['price']<mid_price*(1+tolerance)) & (temp_df['side']=='a')].sort_values(by=['quantity'],ascending=False).head(3)[['EventTime','price','quantity','symbol','side']]
        nbb = lb['price'].max()
        nbo = ub['price'].min()
        mid_price = (nbb+nbo)/2
        spread = nbo-nbb
        df = pd.concat([lb,ub],axis=0)
        d[k]=df.reset_index(drop=True)
        dd[k]={'mid_price':mid_price,'spread':spread,'nbb':nbb,'nbo':nbo}
        print(pd.DataFrame(dd).T.to_markdown())
        

# dict_of_df = {k: pd.DataFrame(v) for k,v in d.items()}
# df = pd.concat(dict_of_df, axis=0)
### keep it simple, set limit bids at the highest quantity. keep updating when 

async def call_api(msg):
    async with websockets.connect(socket,ssl=True,ping_interval=None) as ws:
        await ws.send(msg)
        while True:
            response = await ws.recv()
            await asyncio.sleep(0.1)
            asyncio.create_task(do_something(response=response))
            
asyncio.run(call_api(json.dumps(msg)))
