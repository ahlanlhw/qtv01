import websocket,json
import pandas as pd
cc = input('Running DOM... \n Which Crypto Currency do you want? e.g. CELRUSDT: ')
interval = input("Which Interval do you want? eg. 100 or 1000: ")
tolerance = float(input("What's the tolerance you want? tolerance = 0.02 is 2.00%"))
# socket=f"wss://stream.binance.com:9443/ws/{cc}@kline_{interval}"
socket=f"wss://stream.binance.com:9443/ws"
# o,h,l,c,v = [],[],[],[],[]

def arrange_order_book(data):
    if "order_book" not in globals():
        global order_book
        order_book = pd.DataFrame()
    else:
        order_book = pd.concat([order_book,data],axis=0,ignore_index=True)
        order_book = order_book.sort_values(by=['price'],ascending=False).drop_duplicates(subset=data.columns.difference(['event_id','time','quantity','side']),keep='first')
        order_book = order_book[order_book['quantity']!=0]
        return order_book
def on_open(self):
    print("opened")
    message = {
        "method": "SUBSCRIBE",
        "params":
        [
         f"{cc}@depth@{interval}ms"
         ],
        "id": 1
        }
    ws.send(json.dumps(message))

def on_message(ws,message):
    from numpy.core.fromnumeric import mean
    global tolerance,data
    results = json.loads(message)
    ba = {side: pd.DataFrame(data=results[side], columns=["price", "quantity"],dtype=float)for side in ["b", "a"]}
    ba_list = [ba[side].assign(side=side) for side in ba]
    data = pd.concat(ba_list, axis="index", ignore_index=True, sort=True)
    data['event_id'] = str(results['u'])
    data['time'] = str(results['E'])
    data = data[['event_id','time','price','quantity','side']]
    order_book = arrange_order_book(data)
    # print(order_book)
    # order_book.to_csv('order_book.csv',index=False,index_label=False,header=True)
    try:
        t = order_book[order_book['side']=='a'].iloc[-1]['time']
        nbo =order_book[order_book['side']=='a'].sort_values(by=['price'],ascending=True)
        nbo_p = nbo.iloc[0]['price']
        nbo_q = nbo.iloc[0]['quantity']
        nbb =order_book[order_book['side']=='b'].sort_values(by=['price'],ascending=False)
        nbb_p = nbb.iloc[0]['price']
        nbb_q = nbb.iloc[0]['quantity']
        print(f"Time Now: {t}\n\nCurrent Bid:\n{nbb_p} x {nbb_q};\n\nCurrent Ask:\n{nbo_p} x {nbo_q}\n")
        
        mid_price = (nbo_p+nbb_p)/2
        spread = nbo_p-nbb_p
        print(f"Mid Price:{mid_price:.8f};\nSpread:{spread:.8f}\n")
        # print(f"Mean Price:{order_book['price'].mean()};\nMean Quantity:{order_book['quantity'].mean()}\n")
        upper_bound = nbo[nbo['price']<mid_price*(1+tolerance)]
        lower_bound = nbb[nbb['price']>mid_price*(1-tolerance)]
        largest_bid = lower_bound.sort_values(by='quantity',ascending=False).iloc[0:3][['price','quantity']].sort_values(by='price',ascending=True)
        largest_offer = upper_bound.sort_values(by='quantity',ascending=False).iloc[0:3][['price','quantity']].sort_values(by='price',ascending=True)
        print(f"{tolerance*100:.2f}%_Largest Bid:\n{largest_bid};\n\n{tolerance*100:.2f}%_Largest Ask:\n{largest_offer}\n")
        print(f"depth of book is {len(order_book)}\n#####################\n")
    except Exception as e:
        print(e)
    
    
# def on_error(ws, err):
#     print("Got a an error: ", err)
#     ws.close()
    # cs = message['k']
    # if cs['x']=='True':
    #     o.append(cs['o'])
    #     h.append(cs['h'])
    #     l.append(cs['l'])
    #     c.append(cs['c'])
    #     v.append(cs['v'])

def on_close(ws):
    ### seems to run forever unless we break the script
    print("Connection Closed")

websocket.setdefaulttimeout(20)
ws = websocket.WebSocketApp(socket,on_open=on_open,on_message=on_message,on_close=on_close) #,on_error=on_error
ws.run_forever()