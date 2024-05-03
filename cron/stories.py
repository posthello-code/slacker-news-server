from services.hacker_news import *
from services.openai import doCompletionWithList, optimizeTextForCompletion
from services.postgres import *

session = init_postgres()

print("getting story from hacker news")
storySql = sqlTemplateFromTopStory(session)

checkDuplicates = session.query(stories).where(stories.title == storySql.title).all()
if len(checkDuplicates) == 0:
    # send the text in a list to open AI so it doesn't exceed max tokens
    completionTextList = optimizeTextForCompletion(storySql.summary)
    storySummary = doCompletionWithList(
        completionTextList,
    )

if len(checkDuplicates) == 0:
    if storySummary[0] == ".":
        storySummary = storySummary[1:]

    print(storySummary)

    storyStmt = stories(
        sourceId=storySql.sourceId, title=storySql.title, summary=storySummary
    )

    session.add(storyStmt)
    session.commit()
else:
    print("duplicate story")

try:
    session.close()
except:
    print("already closed")
