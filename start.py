from flask import Flask
from flask_apscheduler import APScheduler
import requests

app = Flask(__name__)
scheduler = APScheduler()

def get_top_story():
    response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
    topStories = eval(response.text)
    response = requests.get('https://hacker-news.firebaseio.com/v0/item/% s.json?print=pretty' % topStories[0])
    print(response.text)
    return response.text
    
if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    scheduler.add_job(id='fetch_data_job', func=get_top_story, trigger='interval', seconds=3600) # Runs every hour
    app.run()