from flask import Flask
from flask_cors import CORS
from flask import request
import scrape_Leetcode
import scrape_Reddit

app = Flask(__name__)
CORS(app)
def main():
    app.run(port=5000, debug=False)

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

if __name__ == "__main__":
    main()