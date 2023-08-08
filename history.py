import requests as client
from io import BytesIO
import pandas as pd

class History:
    def __init__(self, etfs, seed):
        self.etfs = etfs
        self.PERIODS = (8, 13, 21, 34, 55)
        self.RISK = 0.01
        self.SEED = seed
        self.update_data()
        self.update_momentum()
        self.update_risk()
        self.update_table()
    
    def update_table(self):
        self.table = self.etfs\
            .join(self.momentum)\
            .join(self.risk)
        self.table['위험조정모멘텀'] \
            = self.table.momentum * self.table.risk * 252
        self.table['투자유닛']\
            = (self.table.risk * self.SEED)\
                .apply(lambda x: round(x // 5 // 100_000) * 100_000)
        self.table.rename(columns={
            'itemname':'종목명'
        }, inplace=True)
        self.table = self.table\
            .loc[:, ['종목명', '위험조정모멘텀', '투자유닛']]\
            .sort_values('위험조정모멘텀', ascending=False)\
            .loc[self.table.위험조정모멘텀 > 0].head()
        self.table.index.name = '종목코드'
    
    def update_data(self):
        self.data = {
            itemcode: History.get_history(itemcode)
            for itemcode in self.etfs.index
        }
    
    def update_risk(self):
        risk = {
            itemcode: self.get_risk(itemcode)
            for itemcode in self.etfs.index
        }
        self.risk = pd.DataFrame(
            {'itemcode': risk.keys(),
             'risk': risk.values()}
        ).set_index('itemcode')

    def get_risk(self, code):
        data = self.data[code]
        th = pd.concat([data.Close.shift(1), data.High], axis=1).max(axis=1)
        tl = pd.concat([data.Close.shift(1), data.Low], axis=1).min(axis=1)
        tr = th - tl
        atr = tr.ewm(max(self.PERIODS)).mean()
        aatr = atr / data.Close
        return min(1, self.RISK / aatr.iloc[-1])

    def update_momentum(self):
        momentum = {
            itemcode: self.get_momentum(itemcode)
            for itemcode in self.etfs.index
        }
        self.momentum = pd.DataFrame(
            {'itemcode': momentum.keys(),
             'momentum': momentum.values()}
        ).set_index('itemcode')
    
    def get_momentum(self, code):
        score = 0
        scoring = lambda x: x[-1] / x[0] - 1
        for period in self.PERIODS:
            score += self.data[code].Close.rolling(period).apply(scoring).iloc[-1] / period
        return score 

    @classmethod
    def get_history(cls, code):
        URL = 'https://api.finance.naver.com/siseJson.naver'
        params = dict(
            symbol=code,
            requestType=1,
            startTime='19990101',
            endTime='20991231',
            timeframe='day'
        )
        content = client.get(URL, params).content
        df = pd.read_csv(BytesIO(content)).iloc[:-1, 0:5]
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close']
        df.Date = df.Date.str.extract(r'(\d{8})')
        df.Date = pd.to_datetime(df.Date).dt.date
        df.set_index('Date', inplace=True)
        return df