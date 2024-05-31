import json
from services.postgres import init_postgres, close_session
from models.data_models import Source, Comment
from services.openai import doCompletionWithSystemMessage, optimizeTextForCompletion

session = init_postgres()

print("summarize the comments")

comment_sources = (
    session.query(Source)
    .order_by("createdDate")
    .where(Source.source == "hacker-news-comments")
    .all()
)

latest_comments = json.dumps(comment_sources[0].content)

print(latest_comments)
text = optimizeTextForCompletion(latest_comments)
summary = doCompletionWithSystemMessage(
    text,
    """You are being provided comment data for a hacker news article, summarize general sentiment. 
    Provide a few interesting quotes.
    Limit the length to 250 characters""",
)

print(summary)

existing_comments = session.query(Comment).where(
    Comment.sourceId == comment_sources[0].id
)
if len(existing_comments.all()) == 0:
    session.add(Comment(summary=summary, sourceId=comment_sources[0].id))
    session.commit()
else:
    print("update existing")
    session.query(Comment).where(Comment.sourceId == comment_sources[0].id).update(
        {Comment.summary: summary}, synchronize_session=False
    )
    session.commit()

close_session(session)
