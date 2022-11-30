import websocket,json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import style
import time
import numpy as np
import sys
import warnings
sys.tracebacklimit=0
warnings.filterwarnings("module", category=RuntimeWarning) 
cc = input('Running live Chart... \n Which Crypto Currency do you want? e.g. CELRUSDT: ')
interval = input("Which Interval do you want? eg. 100 or 1000: ")
# global duration
# duration = input("How many frames? eg. Between 30 to 120: ")
socket=f"wss://stream.binance.com:9443/ws"
def on_open(self):
    print("opened")
    global event_id_list,bid_list,ask_list,spread_list,vwap_list,fig,axes, time_list,l1,l2,l3
    event_id_list,bid_list,ask_list,spread_list,vwap_list,time_list = [],[],[],[],[],[]
    message = {
        "method": "SUBSCRIBE",
        "params":
        [
        #  "celrusdt@kline_3m",
         f"{cc}@depth20@{interval}ms"
         ],
        "id": 1
        }
    ws.send(json.dumps(message))
    plt.ion()       # Enable interactive mode
    fig = plt.figure()  # Create figure
    axes = fig.add_subplot(111) # Add subplot (dont worry only one plot appears)
    axes.set_autoscale_on(True) # enable autoscale
    axes.autoscale_view(True,True,True)
    l1, = axes.plot([],[], 'r--',label='vwap') # Plot blank data
    l2, = axes.plot([],[], 'g-',label='bid') # Plot blank data
    l3, = axes.plot([],[], 'b-',label='ask') # Plot blank data
    axes.ticklabel_format(style="plain",useOffset=False,axis='both')
    return l1,l2,l3
def animate(frame,l1,l2,l3):
    frame=300
    l1.set_data(time_list[-frame:],vwap_list[-frame:])
    l2.set_data(time_list[-frame:],bid_list[-frame:])
    l3.set_data(time_list[-frame:],ask_list[-frame:])
    # axes.plot(time_list[ln:],vwap_list[ln:], 'r-',label='vwap') # Plot blank data
    # axes.plot(time_list[ln:],bid_list[ln:], 'g-',label='vwap') # Plot blank data
    # axes.plot(time_list[ln:],ask_list[ln:], 'b-',label='vwap') # Plot blank data
    # l2, = plt.plot([],[], 'g-',label='bid') # Plot blank data
    # l3, = plt.plot([],[], 'b-',label='ask') # Plot blank data
    # l.set_data(x1,y1) # update data
    # l2.set_data(ld,lb) # update data
    # l3.set_data(ld,lc) # update data
    # return [l1,l2,l3]
def on_message(ws,message):
    global results
    results = json.loads(message)
    ba = {side: pd.DataFrame(data=results[side], columns=["price", "quantity"],dtype=float)for side in ["bids", "asks"]}
    ba_list = [ba[side].assign(side=side) for side in ba]
    data = pd.concat(ba_list, axis="index", ignore_index=True).sort_values(by=['price'])
    nbb = data[data['side']=='bids'].max().iloc[0]
    nbo = data[data['side']=='asks'].min().iloc[0]
    spread = nbo-nbb
    data['dollarvolume'] = data['price'] * data['quantity']
    vwap = data['dollarvolume'].sum() / data['quantity'].sum()
    bid_list.append(float(nbb))
    ask_list.append(float(nbo))
    vwap_list.append(float(vwap))
    spread_list.append(float(spread))
    event_id_list.append(results['lastUpdateId'])
    time_list.append(time.time())
    axes.relim()        # Recalculate limits
    axes.autoscale_view()#Autoscale
    # if len(time_list)>2:
    ani = FuncAnimation(fig,animate,frames=np.arange(30),interval=len(time_list)+1,blit=True,fargs=[l1,l2,l3])
    plt.pause(0.001)
    if len(event_id_list)<2:
        plt.title(cc)
        plt.legend()
        plt.xticks(rotation=45)
def on_close(ws):
    ### seems to run forever unless we break the script
    print("Connection Closed")

ws = websocket.WebSocketApp(socket,on_open=on_open,on_message=on_message,on_close=on_close) #,on_error=on_error
ws.run_forever()