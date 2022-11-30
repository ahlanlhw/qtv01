### to investigate how I can run this forever
import asyncio,websockets,json,os
from api_caller import call_api
import pandas as pd
cc = 'btcusdt'
request_string = f'!miniTicker@arr'
socket=f"wss://stream.binance.com:9443/ws/" + request_string
msg = {
        "method": "SUBSCRIBE",
        "params":
        [f"{request_string}"],
        "id":1}

async def do_something(response):
    global results
    results = json.loads(response)
    results = pd.DataFrame(results)
    results['q'] = pd.to_numeric(results['q'])
    results = results.sort_values(by='q',ascending=False)
    results = results[results['s'].str[-4:].str.contains('USDT')]
    results = results[~results['s'].str.contains('|'.join(['AUD','EUR','TRY','GBP','UP','DOWN']))].reset_index(drop=True)
    results = results[results['q']>results['q'].median()]
    results.to_csv('miniTicker.csv',index=False)

async def call_api(msg):
    async with websockets.connect(socket,ssl=True,ping_interval=None) as ws:
        await ws.send(msg)
        while True:
            response = await ws.recv()
            await asyncio.sleep(0.00001)
            asyncio.create_task(do_something(response=response))
            # print(results)

asyncio.run(call_api(json.dumps(msg)))
