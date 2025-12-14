from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_db

follow = Blueprint("follow", __name__)

@follow.route("/api/follow/<int:uid>", methods=["POST"])
@jwt_required()
def follow_user(uid):
    user_id = get_jwt_identity()

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "INSERT IGNORE INTO follows (follower_id, following_id) VALUES (%s, %s)",
        (user_id, uid)
    )

    db.commit()
    db.close()

    return jsonify({
        "status": "success",
        "action": "followed",
        "user_id": uid
    })


@follow.route("/api/unfollow/<int:uid>", methods=["POST"])
@jwt_required()
def unfollow_user(uid):
    user_id = get_jwt_identity()

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "DELETE FROM follows WHERE follower_id=%s AND following_id=%s",
        (user_id, uid)
    )

    db.commit()
    db.close()

    return jsonify({
        "status": "success",
        "action": "unfollowed",
        "user_id": uid
    })
