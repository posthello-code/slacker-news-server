import json

from sqlalchemy import desc
from services.postgres import init_postgres, close_session
from models.data_models import Source, Comment
from services.openai import doCompletionWithSystemMessage, optimizeTextForCompletion

session = init_postgres()

comment_sources = (
    session.query(Source)
    .order_by(desc("createdDate"))
    .where(Source.source == "hacker-news-comment")
    .all()
)

latest_comments_obj = comment_sources[0]
latest_comments = json.dumps(latest_comments_obj.content)
# print(latest_comments)
text = optimizeTextForCompletion(latest_comments)
summary = doCompletionWithSystemMessage(
    text,
    """You are being provided comment data for a hacker news article, summarize general sentiment. 
    Provide a few interesting quotesfrom the comments verbatim.
    Limit the length to 250 characters.
    Don't repeat yourself""",
)

print(summary)

existing_comments = session.query(Comment).where(
    Comment.sourceId == latest_comments_obj.id
)
if len(existing_comments.all()) == 0:
    session.add(
        Comment(
            summary=summary,
            sourceId=latest_comments_obj.id,
            externalId=latest_comments_obj.externalId,
        )
    )
    session.commit()
else:
    print("update existing")
    session.query(Comment).where(Comment.sourceId == latest_comments_obj.id).update(
        {Comment.summary: summary}, synchronize_session=False
    )
    session.commit()

close_session(session)
