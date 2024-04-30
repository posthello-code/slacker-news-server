from services.hacker_news import *
from services.postgres import *

session = init_postgres()

story = get_top_story()

# model for story to insert into db
story = stories(story=story)
# save to postgres
session.add(story)
session.commit()

try:
  session.close()
except:
  print("already closed")


