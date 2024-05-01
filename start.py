from flask import Flask
from flask_restful import Api
from services.postgres import init_postgres, sources, stories
from flask_restful import fields, marshal_with


session = init_postgres()
app = Flask(__name__)
api = Api(app)


@app.route("/stories")
@marshal_with(
    {
        "id": fields.String,
        "createdDate": fields.String,
        "sourceId": fields.String,
        "title": fields.String,
        "summary": fields.String,
    }
)
def get_stories():
    items = session.query(stories).all()
    return items


@app.route("/sources")
@marshal_with(
    {
        "id": fields.String,
        "source": fields.String,
        "createdDate": fields.String,
        "sourceMethod": fields.String,
        "sourceUri": fields.String,
        "content": fields.String,
    }
)
def get_sources():
    items = session.query(sources).order_by("createdDate").all()
    return items


if __name__ == "__main__":
    app.run(debug=False)
