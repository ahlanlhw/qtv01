import os
import pandas as pd
import datetime,io,time
fp = os.getcwd()+'\\streams\\'
interval = 30
while True:
    for k in os.listdir(fp):
        df = pd.read_csv(fp+k,header='infer')
        
        df['sequential'] = df['cml_vol'].rolling(interval).sum()/df['cml_vol'].rolling(interval*2).sum()*100-100
        df['jerk'] = df['sequential'].rolling(interval).sum()/df['sequential'].rolling(interval*2).sum()*100-100
        df = df.dropna(subset=['sequential','jerk'])
        print(df.iloc[-1])
        time.sleep(0.2)

    # df.to_csv('study.csv',index=False)
        