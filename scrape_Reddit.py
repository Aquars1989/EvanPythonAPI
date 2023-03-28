import requests
from bs4 import BeautifulSoup as bs4
import click
import pandas as pd
from fake_useragent import UserAgent
import json

@click.command()
def main():
    print(getData('technology'))
    pass

def getData(subreddit,lastThing=""):
    try:
        #print(tag,lastThing)
        url=f'https://old.reddit.com/r/{subreddit}/new/' + ("?count=25&after="+lastThing if lastThing!="" else "")
        
        #headers = {
        #"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
        #"Accept-Encoding": "gzip, deflate, br", 
        #"Accept-Language": "zh-TW,zh;q=0.9", 
        #"Host": url,  
        #"Sec-Fetch-Dest": "document", 
        #"Sec-Fetch-Mode": "navigate", 
        #"Sec-Fetch-Site": "none", 
        #"Upgrade-Insecure-Requests": "1", 
        #"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36" #使用者代理
        #}
        user_agent=UserAgent()
        response=requests.get(url, headers={ 'user-agent': user_agent.random} )

        soup=bs4(response.text,"lxml")
        title=soup.select("div.linkflair a.title")
        author=soup.select("div.linkflair p.tagline")
        time=soup.select("time.live-timestamp")
        thing=soup.select("div.linkflair.thing")
        
        #print("title:"+str(len(title)))
        #print("author:"+str(len(author)))
        #print("time:"+str(len(time)))
        #print("thing:"+str(len(thing)))

        if(len(title)==0):
            return {"code":"0000","message":"Ok","data":[]}

        list=[]
        for i in range(len(title)):
            authorInner=author[i].select("a.author")
            if(len(authorInner)==0):
                authorInner=author[i].select("span")
            list+=[[title[i]["href"],title[i].text,authorInner[0].text,time[i].text,thing[i]["data-fullname"]]]
            
        df=pd.DataFrame(list,columns=["url","title","author","time","thing"])
        jtagRes = json.loads(df.to_json(orient='records'))

        res= {"code":"0000","message":"Ok","data":jtagRes}
        return res
    except Exception as msg:
        return {"code":"E990","message":msg}

if __name__ == "__main__":
    main()