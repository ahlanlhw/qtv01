import asyncio,websockets,json
cc = 'bnbusdt'
request_string=f'{cc}@bookTicker'
# /stream?streams="
socket=f"wss://stream.binance.com:9443/ws/" + request_string
msg = {
        "method": "SUBSCRIBE",
        "params":
        [f"{request_string}"],
        "id":1}
async def do_something(response):
    results = json.loads(response)
    print(results)

async def call_api(msg):
    async with websockets.connect(socket,ssl=True,ping_interval=None) as ws:
        await ws.send(msg)
        while True:
            response = await ws.recv()
            await asyncio.sleep(0.00001)
            # results = json.loads(response)
            asyncio.create_task(do_something(response=response))
asyncio.run(call_api(json.dumps(msg)))