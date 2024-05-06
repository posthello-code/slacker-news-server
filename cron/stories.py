from services.hacker_news import *
from services.openai import doCompletionWithSystemMessage
from services.postgres import *

session = init_postgres()

print("getting story from hacker news")
storySql = sqlTemplateFromTopStory(session)

checkDuplicates = session.query(stories).where(stories.title == storySql.title).all()
if len(checkDuplicates) == 0:
    storySummary = doCompletionWithSystemMessage(
        storySql.summary,
        """You are a tech news and blog 
        writer. You will simplify technical jargon 
        so that the average technologist will 
        understand. Given an html doc, use only 
        only the article text, ignore the 
        tags. Summarize and shorten the content.
        Separate similar sections into separate paragraphs 
        If the provided text does not 
        provide enough useful text respond with 
        the character '.'""",
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
