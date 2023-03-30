import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json

def main():
    print(getData())
    pass

def getData():
    user_agent=UserAgent()
    r=requests.get(f'https://finance.yahoo.com/crypto/', headers={ 'user-agent': user_agent.random} )
    soup=BeautifulSoup(r.text,"lxml")
    data=[]
    trs= soup.select('tr')
    for tr in trs:
        tds=tr.select('td')
        if len(tds)<5:
            continue
        val=[tds[0].text,tds[2].text,tds[3].text,tds[4].text]
        data.append(val)
    dataRes=pd.DataFrame(data,columns=["name","price","change","changeRate"]).to_json(orient='records')
    jdataRes = json.loads(dataRes)
    res= {"code":"0000","message":"Ok","data": jdataRes}
    return res

if __name__ == "__main__":
    main()