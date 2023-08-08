import pandas as pd
import requests as client

class Universe:
    def __init__(self):
        self.get_selected_etfs()
        self.get_etf_item_list()
        self.table = pd.merge(self.selected,
                        self.etf_item_list)\
                .sort_values('marketSum', ascending=False)\
                .set_index('itemcode')
    
    def get_selected_etfs(self):
        self.selected = pd.read_csv('etfs.csv', dtype=str)

    def get_etf_item_list(self):
        URL = 'https://finance.naver.com/api/sise/etfItemList.nhn'
        params = dict(
            etfType=0,
            targetColumn='market_sum',
            sortOrder='desc'
        )
        json : dict = client.get(URL, params).json()
        result = json.get('result').get('etfItemList')
        self.etf_item_list = pd.DataFrame(result)[['itemcode', 'itemname', 'marketSum']]

