import requests
import json
import PIL
import unidecode

LISTINGS =["hot","new","top","rising","random","controversial"]
WORD_LENGTH = 2193
WORDS_PER_SECOND = 2.81
VIDEO_LENGTH = 780 #13 Minutes

def raw_reddit_json(subreddit, listing,amount=15):
    if listing in LISTINGS:
        url = "https://www.reddit.com/r/"+subreddit+"/"+listing+".json"
        params = (
            ('count', 1),
            ('limit', amount)
        )
        response = requests.get('https://www.reddit.com/r/entitledparents/top.json', params=params, headers = {'User-agent': 'downloadScript'}).json()
        return response
    else:
        print("Invalid Listing option")
        return False

"""
#Getter Functions for Reddit. Hand it the raw reddit json at whichever element you want.
"""
def get_score(post):
    return post['data']['score']
    
def get_selftext(post):
    return post['data']['selftext']

def get_title(post):
    return post['data']['title']
    
def pretty_write_json(json,out):
    json = json.dumps(json, indent=4, sort_keys=True)
    with open(out, 'w') as outfile: 
        outfile.write(json)

def get_word_count(story):
    return len(story.split())

def return_stories_amount(subreddit,listing,wordcount=(VIDEO_LENGTH*WORDS_PER_SECOND)): #returns amount of stories
    response = raw_reddit_json(subreddit,listing)
    count = 0
    current_words = 0
    for i in response['data']['children']:        
        current_words += get_word_count(get_selftext(i))
        count += 1
        if current_words >= wordcount:
            break
    return count
    
#MAIN function    
if __name__ == '__main__':
    print (return_stories_amount("pettyrevenge","hot"))