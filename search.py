from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from db import get_db

search = Blueprint("search", __name__)

@search.route("/api/search")
@jwt_required()
def search_users():
    q = request.args.get("q", "")
    db = get_db()
    cur = db.cursor()

    cur.execute(
        "SELECT id, username FROM users WHERE username LIKE %s LIMIT 10",
        (f"%{q}%",)
    )

    users = cur.fetchall()
    db.close()
    return jsonify(users)
