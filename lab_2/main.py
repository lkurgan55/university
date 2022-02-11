import os
import pandas as pd

# отримання курсу за 2021 рік
if os.path.isfile("data.csv"):
    df = pd.read_csv("data.csv")
else:
    #створення списку потрібних дат
    df = pd.DataFrame({"date":[], 'USD':[], 'EUR':[]})
    dates = pd.Series(pd.date_range(start='1/1/2021', end='12/31/2021', freq='d'))
    dates = dates.dt.strftime('%Y%m%d')
    for date in dates:
        df_t = pd.read_json(f'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date={date}&json')
        df_t = pd.DataFrame({"date":df_t[df_t['cc']=="USD"]['exchangedate'].values, 'USD':df_t[df_t['cc']=="USD"]['rate'].values, 'EUR':df_t[df_t['cc']=="EUR"]['rate'].values})
        df = pd.concat([df,df_t], axis=0)

    df = df.reset_index(drop=True)
    df.to_csv("data.csv", index=False)

print(df.head())
print(df.tail())


