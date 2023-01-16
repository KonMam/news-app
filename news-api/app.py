from flask import Flask, jsonify, render_template, request
from sqlite import SQLite
from db import init_db


def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    init_db(app)
    return app


app = create_app()


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/articles", methods=["GET"])
def articles():
    args = request.args
    title = '%' + args.get("title", default="", type=str) + '%'
    page = '%' + args.get("page", default="", type=str) + '%'

    try:
        with SQLite('news.db') as cur:
            cur.execute(
                """
                SELECT
                    *
                FROM
                    articles
                WHERE
                    title LIKE ? and
                    page LIKE ?
                """,
                (title, page,)
            )
            result = cur.fetchall()
            return jsonify(result)
    except Exception as e:
        return {"status": "failure", "error": e}
