# ### isbuyermaker = False ->>> means the buyer(bidder) bought at the ask, implying bullish. We can check for each trade at the dollar volume when they buy.
# ### next step is to run multi
### to investigate how I can run this forever
import asyncio,websockets,json,time,os,datetime
import pandas as pd
### for multiple streams
# ticker_list = ['ethusdt','btcusdt','bnbusdt']
# request_string = str('@aggTrade,'.join(ticker_list))[:-1]
# request_string = request_string.split(',')
# socket=f"wss://stream.binance.com:9443/stream?streams=" + "/".join(request_string) ###

cc = 'ftmusdt'
fn = f'{os.getcwd()}\\streams\\{cc}_tradeStream.csv'
request_string = f'{cc}@aggTrade'
socket=f"wss://stream.binance.com:9443/ws/" + request_string
d={}
cml_vol = float() 
cml_bid = int()
cml_vol_l,cml_bid_l = [],[]
msg = { "method": "SUBSCRIBE",
        "params":
        [request_string],
        # [f"{request_string}"],
        "id":1}

async def do_something(response):
    global results,df,cml_vol,cml_bid,d,cml_vol_l,cml_bid_l,cml_vol_seq,cml_bid_seq,whale_sig
    results = json.loads(response)
    df = pd.DataFrame(results,index=[0])
    column_naming ={"E":"EventTime","s":"Symbol",'a':"aggTradeID","p":'price','q':"quantity",'m':"bidderMaker"}
    df = df[list(column_naming.keys())].rename(columns = column_naming)
    df['priceTimesQuantity'] = df['price'].astype(float) * df['quantity'].astype(float)
    df['priceTimesQuantity'] = df.apply(lambda x: x['priceTimesQuantity']*-1 if x['bidderMaker'] == True else x['priceTimesQuantity'],axis=1)
    df['EventTime'] = df['EventTime'].apply(lambda x:datetime.datetime.fromtimestamp(x/1000))
    df = df.sort_values(by='EventTime',ascending=True)
    cml_vol +=df['priceTimesQuantity'].iloc[-1]
    df['cml_vol'] = cml_vol
    df['sig'] =df.apply(lambda x: -1 if x['bidderMaker'] == True else 1,axis=1)
    cml_bid+=df['sig'].iloc[-1]
    df['cml_bid'] = cml_bid
    d.update(df.to_dict())
    ### test volume first
    cml_vol_l.append(cml_vol)
    cml_bid_l.append(cml_bid)
    if len(cml_vol_l) > 60:
        cml_vol_seq = pd.Series(cml_vol_l).rolling(30).mean()/pd.Series(cml_vol_l).rolling(60).mean()*100-100
        cml_bid_seq = pd.Series(cml_bid_l).rolling(30).mean()/pd.Series(cml_bid_l).rolling(60).mean()*100-100
        whale_sig = cml_bid_seq.diff()-cml_vol_seq.diff()
        whale_sig = whale_sig.dropna().to_list()
        cml_vol_seq = cml_vol_seq.diff().dropna().to_list()
        cml_bid_seq = cml_bid_seq.diff().dropna().to_list()
    
    if len(cml_vol_l)>1800:
        cml_vol_l = cml_vol_l[-1800:]
        cml_bid_l = cml_bid_l[-1800:]
    if os.path.isfile(fn):
        load_saved_csv = pd.read_csv(fn,header='infer')
        if load_saved_csv.empty:
            pd.DataFrame.from_dict(d).reset_index(drop=True).iloc[-1800:].to_csv(fn,index=False)
        else:
            load_saved_csv = pd.concat([load_saved_csv,pd.DataFrame.from_dict(d)],axis=0).reset_index(drop=True)
            load_saved_csv.reset_index(drop=True).iloc[-1800:].to_csv(fn,index=False)
    else:
        pd.DataFrame.from_dict(d).iloc[-1800:].reset_index(drop=True).to_csv(fn,index=False)
    await asyncio.sleep(5)
    print(df[['Symbol','EventTime','price','quantity','bidderMaker',"priceTimesQuantity",'cml_vol','cml_bid']].iloc[-1])
    if "cml_vol_seq" in globals():
        print(f"Buying {cc} if Whale_Signal > 0 & whale_sig[-1] > whale_sig[-2]")
        print(f"Sequential Cumulative Volume is {cml_vol_seq[-3:]}")
        print(f"Sequential Cumulative Bid is {cml_bid_seq[-3:]}")
        print(f"Sequential Whale_Signal is {whale_sig[-3:]}")

async def call_api(msg):
    async with websockets.connect(socket,ssl=True,ping_interval=None) as ws:
            await ws.send(msg)
            while True:
                response = await ws.recv()
                await asyncio.sleep(0.00001)
                asyncio.create_task(do_something(response=response))

asyncio.run(call_api(json.dumps(msg)))
## pandas groupby stream
# {
#   "e": "aggTrade",  // Event type
#   "E": 123456789,   // Event time
#   "s": "BNBBTC",    // Symbol
#   "a": 12345,       // Aggregate trade ID
#   "p": "0.001",     // Price
#   "q": "100",       // Quantity
#   "f": 100,         // First trade ID
#   "l": 105,         // Last trade ID
#   "T": 123456785,   // Trade time
#   "m": true,        // Is the buyer the market maker?
#   "M": true         // Ignore
# }

### if bidder is maker is False -> they bought market order at the ask crossing the spread, if True, $Volume x -1