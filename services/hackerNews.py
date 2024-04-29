import requests

def getTopStory():
    response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
    topStories = eval(response.text)
    response = requests.get('https://hacker-news.firebaseio.com/v0/item/% s.json?print=pretty' % topStories[0])
    print(response.text)
    return response.text