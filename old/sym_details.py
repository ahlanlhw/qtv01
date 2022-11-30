import asyncio,json

# cc="algousdt"
async def sym_details(cc):
    from binance import AsyncClient
    global symbol_info
    client = await AsyncClient.create()
    symbol_info = await client.get_symbol_info(f"{cc}")
    # print(json.dumps(symbol_info, indent=2))
    # print(symbol_info['filters'][0]['tickSize'])
    await client.close_connection()
    return symbol_info
# async def run_func(sym_details(cc)):
#     await sym_details(cc)
# if __name__ == "__main__":
#     # asyncio.run(run_func)
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(sym_details(cc))

# symbol_info
