import os
from flask import Flask
from flask_cors import cross_origin
from flask_restful import Api
from sqlalchemy import desc
from services.postgres import init_postgres
from models.data_models import Comment, Source, Story
from flask_restful import fields, marshal_with

allowed_origins = [
    "https://slacker-news-frontend.onrender.com",
    "http://localhost*",
]

render_url = os.getenv("RENDER_EXTERNAL_URL")

if render_url:
    allowed_origins.append(render_url)

session = init_postgres()
app = Flask(__name__)
api = Api(app)


@app.route("/stories")
@cross_origin(origins=allowed_origins)
@marshal_with(
    {
        "id": fields.String,
        "createdDate": fields.String,
        "sourceId": fields.String,
        "title": fields.String,
        "summary": fields.String,
        "sourceUri": fields.String,
        "externalId": fields.Integer,
    }
)
def get_stories():
    try:
        items = session.query(Story).order_by(desc("createdDate")).all()
    except:
        session.rollback()
    return items


@app.route("/sources")
@cross_origin(origins=allowed_origins)
@marshal_with(
    {
        "id": fields.String,
        "source": fields.String,
        "createdDate": fields.String,
        "sourceMethod": fields.String,
        "sourceUri": fields.String,
        "content": fields.String,
        "externalId": fields.Integer,
    }
)
def get_sources():
    items = session.query(Source).order_by(desc("createdDate")).all()
    return items


@app.route("/comments")
@cross_origin(origins=allowed_origins)
@marshal_with(
    {
        "id": fields.String,
        "sourceId": fields.String,
        "createdDate": fields.String,
        "summary": fields.String,
        "externalId": fields.Integer,
    }
)
def get_comments():
    items = session.query(Comment).order_by(desc("createdDate")).all()
    return items


@app.route("/")
def root():
    return "OK"


if __name__ == "__main__":
    app.run(debug=False)
