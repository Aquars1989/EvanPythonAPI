import asyncio
import aiohttp
from google.cloud import secretmanager

chars=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def main():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    print(asyncio.run(getData('radi?','Y')))
    pass

async def getData(word,isTranslate):
    try:
        if word.count('?')>4:
            return {"code":"E201","message":"number of unknown letters must less than 5"}

        mask = set()
        with open('WordList.txt') as f:
            lines = f.readlines()
            for l in lines:
                mask.add(l.replace('\n',''))

        words=[]
        __switchChar(word.lower(),words,mask)
        
        resullt=[]
        tasks = []
        if isTranslate.lower()=='y':
            translateKey=access_secret_version('key_azure_translator')

            for w in words:
                tasks.append(asyncio.gather(__translate(w,translateKey), __getDefine(w)))
            results = await asyncio.gather(*tasks)
            for i, w in enumerate(words):
                if i >= len(results):
                    break
                if results[i]:
                    resullt.append({"word":w,"translated":results[i][0],"mean":results[i][1]})
        else:
            for w in words:
                tasks.append(asyncio.gather( __getDefine(w)))
            results = await asyncio.gather(*tasks)
            for i, w in enumerate(words):
                if i >= len(results):
                    break
                if results[i]:
                    resullt.append({"word":w,"mean":results[i][0]})
        return {"code":"0000","message":"Ok","data":resullt}
    except Exception as msg:
        return {"code":"E990","message":msg}

async def __getDefine(word):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}') as resp:
            json = await resp.json()
            res = []
            if type(json)==dict:
                return None
            for mean in json[0]['meanings']:
                part=mean['partOfSpeech']
                limit=3
                for defin in mean['definitions']:
                    if limit <= 0:
                        break
                    res.append(f"[{part}] {defin['definition']}")
                    limit-=1
            return res

async def __translate(word,translateKey):
    data=[{"Text":word}]
    headers={"Content-Type": "application/json","Ocp-Apim-Subscription-Key": translateKey,"Ocp-Apim-Subscription-Region": "eastasia"}
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(session.post(f'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from=en&to=zh-TW',json=data,headers=headers))]
        results = await asyncio.gather(*tasks)
        json = await results[0].json()
        return json[0]['translations'][0]["text"]

def __switchChar(word,result,mask):
    idx=word.find('?')
    if idx>=0:
        for c in chars:
            __switchChar(word[0:idx]+c+word[idx+1:],result,mask)
    elif word in mask:
        result.append(word)
        


def access_secret_version(secret_id, version_id="latest"):
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/732326142772/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(name=name)

    # Return the decoded payload.
    return response.payload.data.decode('UTF-8')
    
if __name__ == "__main__":
    main()