import time
import requests
from fake_useragent import UserAgent
from google.cloud import secretmanager

def main():
    print(getData('A old man'))

def getData(word):
    try:
        user_agent=UserAgent()
        cookie=access_secret_version('cookie_openart')
        data={"prompt":word,"base_model":"runwayml/stable-diffusion-v1-5","version":1.5,"model":"stable_diffusion","width":512,"height":512,"image_num":1,"cfg_scale":7,"negative_prompt":"","steps":25,"sampler":"dpmsolver++","seed":""}
        response=requests.post('https://openart.ai/api/create/stable_diffusion', headers={ 'user-agent': user_agent.random ,'Cookie':cookie},data=data).json()

        if "generation_history_id" not in response:
            raise Exception(response["error"])
        historyId=response["generation_history_id"]
        url=""
        while url=="":
            response=requests.get(f'https://openart.ai/api/create/image_placeholder?generation_history_id={historyId}', headers={ 'user-agent': user_agent.random,'Cookie':cookie }).json()
            url=response["images"][0]["url"]
            time.sleep(0.3)
        res={"code":"0000","message":"Ok","data": url}
        return res
    except Exception as msg:
        return {"code":"E990","message":msg}

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