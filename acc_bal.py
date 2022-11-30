def login():
    import os,json
    import pandas as pd
    from binance.spot import Spot
    from binance.client import Client
    with open('id.txt') as f:
        lines = f.readlines()
        api_key = ''.join(lines).split('\n')[0]
        secret_key = ''.join(lines).split('\n')[1]

    ## login here
    client=Spot()
    client=Spot(key=api_key,secret=secret_key)
    ### details here    
    # Get account information
    bal = pd.DataFrame(client.account()['balances'])
    bal['free'] = pd.to_numeric(bal['free'])
    bal['locked'] = pd.to_numeric(bal['locked'])
    bal['sum'] = bal['free']+bal['locked']
    bal = bal[bal['sum']>0][['asset','free','locked']].reset_index(drop=True)
    print(f"Here's your spot wallet:\n {bal[['asset','free']]}")
    return bal
# import requests,hashlib,json
# url = "https://api1.binance.com/api/v3/"
# sys_status = "https://api1.binance.com/sapi/v1/system/status"
# acc = "https://api.binance.com/api/v3/account"
# coin_info = "https://api1.binance.com//sapi/v1/capital/config/getall"
# ### pings the server
# test = requests.get("https://api.binance.com/api/v1/ping")
# ### gets server time
# servertime = requests.get("https://api.binance.com/api/v1/time")
# print(json.loads(servertime.text)['serverTime'])
# params = {
#             "signature":hashlib.sha256(secret_key)

#             }   
# r = requests.get(coin_info,params=params)
# r.status_code
# qry = ""
# params = {
#     'symbol': 'BTCUSDT',
#     'side': 'BUY',
#     'type': 'LIMIT',
#     'timeInForce': 'GTC',
#     'quantity': 0.002,
#     'price': 9500
# }
# response = Client.new_order_test(params)
# print(response)

# ws = websocket.WebSocketApp(socket,on_open=on_open,on_message=on_message,on_close=on_close) #,on_error=on_error
# ws.run_forever()