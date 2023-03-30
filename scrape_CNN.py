import pandas as pd
import requests
from fake_useragent import UserAgent
import json

def main():
    print(getData("ukraine",0,20))
    pass

def getData(word,skip,size):
    try:
        user_agent=UserAgent()
        response=requests.get(f'https://search.api.cnn.com/content?q={word}&size={size}&from={skip}&page=1&sort=newest', headers={ 'user-agent': user_agent.random}).json()

        data=[]
        for r in response["result"]:
            data.append([r["headline"],r["url"],r["mappedSection"],r["firstPublishDate"],r["lastPublishDate"]])
        df=pd.DataFrame(data,columns=["headline","url","category","firstPublish","lastPublish"])
        dataRes = df[["headline","url","category","firstPublish","lastPublish"]].to_json(orient='records')
        jdataRes = json.loads(dataRes)
        res={"code":"0000","message":"Ok","data": jdataRes}
        return res
    except Exception as msg:
        return {"code":"E990","message":msg}

if __name__ == "__main__":
    main()