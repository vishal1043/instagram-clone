from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_db

comments = Blueprint("comments", __name__)

@comments.route("/api/comment/<int:post_id>", methods=["POST"])
@jwt_required()
def add_comment(post_id):
    user_id = get_jwt_identity()
    text = request.json["text"]

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO comments(user_id, post_id, text) VALUES (%s,%s,%s)",
        (user_id, post_id, text)
    )
    db.commit()
    db.close()

    return jsonify({"status": "success"})
