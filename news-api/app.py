from flask import Flask, jsonify, request
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
    return {"test": "yay"}


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


@app.route("/create_article", methods=["POST"])
def create_article():
    try:
        with SQLite('news.db') as cur:
            data = request.json
            if data:
                cur.execute(
                    'INSERT INTO articles (page, href, title) VALUES(?,?,?)',
                    (data["page"], data["href"], data["title"])
                )
        return jsonify({"status": "success",
                        "data": data})
    except Exception as e:
        return {"status": "failure", "error": e}


@app.route("/delete_article/<id>", methods=["DELETE"])
def delete_article(id):
    try:
        with SQLite('news.db') as cur:
            cur.execute('SELECT * FROM articles WHERE id = ?', (id,))
            result = cur.fetchall()
            cur.execute(
                'DELETE FROM articles WHERE id = ?', (id,)
            )
        return jsonify({"status": "success",
                        "data": result})
    except Exception as e:
        return {"status": "failure", "error": e}
