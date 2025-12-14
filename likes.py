from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_db

likes = Blueprint("likes", __name__)

@likes.route("/api/like/<int:pid>", methods=["POST"])
@jwt_required()
def like_post(pid):
    user_id = get_jwt_identity()

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "INSERT IGNORE INTO likes (user_id, post_id) VALUES (%s, %s)",
        (user_id, pid)
    )

    db.commit()
    db.close()

    return jsonify({
        "status": "success",
        "action": "liked",
        "post_id": pid
    })
