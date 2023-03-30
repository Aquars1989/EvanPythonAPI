import pandas as pd
import requests
from fake_useragent import UserAgent

def main():
    print(getData('BTC-USD'))
    pass

def getData(crypto):
    user_agent=UserAgent()
    r=requests.get(f'https://query1.finance.yahoo.com/v8/finance/chart/{crypto}?region=US&lang=en-US&includePrePost=false&interval=2m&useYfid=true&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance', headers={ 'user-agent': user_agent.random} )
    json=r.json()
    res= {"code":"0000","message":"Ok","data": {"timestamp":json["chart"]["result"][0]["timestamp"],"indicators":json["chart"]["result"][0]["indicators"]}}
    return res

if __name__ == "__main__":
    main()