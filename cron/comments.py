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
text = optimizeTextForCompletion(
    "Any quotes in your output should be verbatim, use the following data: "
    + latest_comments
)
summary = doCompletionWithSystemMessage(
    text,
    """
    You are a comment summarizer.
    Describe the general sentiment of the conversation and
    Provide a few interesting quotes from the provided comments verbatim.
    Limit the length to 250 characters.
    Don't repeat yourself.
    If there is nothing to summarize respond with the character '.'
    """,
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
