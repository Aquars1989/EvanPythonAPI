from flask import Flask
from flask import request
from flask_cors import CORS
import scrape_Leetcode
import scrape_Reddit
import scrabble_Helper
import scrape_CNN
import scrape_Crypto
import scrape_CryptoDetail
import OpenArt_Agent
import asyncio

app = Flask(__name__)
CORS(app)

def main():
    app.run(port=8080, debug=False)

@app.route('/api/scrape_leetcode', methods=['GET'])
def scrape_leetcode():
    skip  = request.args.get('skip', type=int ,default=1)
    limit  = request.args.get('limit', type=int ,default=100)
    return scrape_Leetcode.getData(skip,limit)

@app.route('/api/scrape_reddit', methods=['GET'])
def scrape_reddit():
    subreddit = request.args.get('subreddit', type=str ,default="")
    lastThing = request.args.get('lastThing', type=str ,default="")
    return scrape_Reddit.getData(subreddit,lastThing)

@app.route('/api/scrabble_helper', methods=['GET'])
def scrabble_helper():
    word = request.args.get('word', type=str ,default="")
    isTranslate = request.args.get('translate', type=str ,default="N")
    return asyncio.run(scrabble_Helper.getData(word,isTranslate))

@app.route('/api/scrape_crypto', methods=['GET'])
def scrape_crypto():
    return scrape_Crypto.getData()

@app.route('/api/scrape_crypto_detail', methods=['GET'])
def scrape_crypto_detail():
    crypto = request.args.get('crypto', type=str ,default="")
    return scrape_CryptoDetail.getData(crypto)

@app.route('/api/scrape_cnn', methods=['GET'])
def scrape_cnn():
    word = request.args.get('word', type=str ,default="")
    skip = request.args.get('skip', type=int ,default=0)
    size = request.args.get('size', type=int ,default=10)
    return scrape_CNN.getData(word,skip,size)

#@app.route('/api/openart_agent', methods=['GET'])
#def openart_agent():
#    word = request.args.get('word', type=str ,default="")
#    return OpenArt_Agent.getData(word)

if __name__ == "__main__":
    main()