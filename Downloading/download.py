import requests
import json
import PIL
import unidecode

LISTINGS =["hot","new","top","rising","random","controversial"]

def raw_reddit_json(subreddit, listing,amount):
    if listing in LISTINGS:
        url = "https://www.reddit.com/r/"+subreddit+"/"+listing+".json"
        params = (
            ('count', amount),
        )
        response = requests.get('https://www.reddit.com/r/entitledparents/top.json', params=params, headers = {'User-agent': 'downloadScript'}).json()
        return response
    else:
        print("Invalid Listing option")
        return False

def get_score(post):
    return post['data']['score']
    
def get_selftext(post):
    return post['data']['selftext']

def get_title(post):
    return post['data']['title']
    
def pretty_write_json(json,out):
    with open(out, 'w') as outfile: 
        outfile.write(json)



response = raw_reddit_json("entitledparents","top","3")

for i in response['data']['children']:
    print(i['data']['score'])

"""
response = json.dumps(response, indent=4, sort_keys=True)




with open('post.json', 'w') as outfile: 
    outfile.write(response)
    
"""    