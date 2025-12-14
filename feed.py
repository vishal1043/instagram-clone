from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_db

feed = Blueprint("feed", __name__)

# @feed.route("/api/profile", methods=["GET"])
# @jwt_required()
# def get_profile():
#     me = get_jwt_identity()
#     db = get_db()
#     cur = db.cursor()

#     cur.execute("SELECT id, username, profile_photo FROM users WHERE id=%s", (me,))
#     user = cur.fetchone()

#     cur.execute("SELECT COUNT(*) AS cnt FROM posts WHERE user_id=%s", (me,))
#     posts = cur.fetchone()["cnt"]

#     cur.execute("SELECT COUNT(*) AS cnt FROM follows WHERE follower_id=%s", (me,))
#     following = cur.fetchone()["cnt"]

#     cur.execute("SELECT COUNT(*) AS cnt FROM follows WHERE following_id=%s", (me,))
#     followers = cur.fetchone()["cnt"]

#     cur.execute("""
#         SELECT id, image_url, caption
#         FROM posts
#         WHERE user_id=%s
#         ORDER BY created_at DESC
#     """, (me,))
#     user_posts = cur.fetchall()

#     db.close()

#     return jsonify({
#         "user": user,
#         "stats": {
#             "posts": posts,
#             "followers": followers,
#             "following": following
#         },
#         "posts": user_posts
#     })

@feed.route("/api/profile", methods=["GET"])
@jwt_required()
def get_profile():
    me = get_jwt_identity()
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT id, username, profile_photo FROM users WHERE id=%s", (me,))
    user = cur.fetchone()

    cur.execute("SELECT COUNT(*) AS cnt FROM posts WHERE user_id=%s", (me,))
    posts = cur.fetchone()["cnt"]

    cur.execute("SELECT COUNT(*) AS cnt FROM follows WHERE follower_id=%s", (me,))
    following = cur.fetchone()["cnt"]

    cur.execute("SELECT COUNT(*) AS cnt FROM follows WHERE following_id=%s", (me,))
    followers = cur.fetchone()["cnt"]

    cur.execute("""
        SELECT 
          p.id,
          p.image_url,
          p.caption,
          (SELECT COUNT(*) FROM likes WHERE post_id=p.id) AS like_count,
          (SELECT COUNT(*) FROM comments WHERE post_id=p.id) AS comment_count
        FROM posts p
        WHERE p.user_id=%s
        ORDER BY p.created_at DESC
    """, (me,))

    user_posts = cur.fetchall()
    db.close()

    return jsonify({
        "user": user,
        "stats": {
            "posts": posts,
            "followers": followers,
            "following": following
        },
        "posts": user_posts
    })



@feed.route("/api/feed", methods=["GET"])
@jwt_required()
def get_feed():
    me = get_jwt_identity()

    db = get_db()
    cur = db.cursor()   # ✅ FIXED (no dictionary=True)

    cur.execute("""
        SELECT
            p.id AS post_id,
            p.image_url,
            p.caption,
            u.id AS user_id,
            u.username,
            u.profile_photo,
            IF(f.follower_id IS NULL, 0, 1) AS is_following,
            (SELECT COUNT(*) FROM likes WHERE post_id=p.id) AS like_count
        FROM posts p
        JOIN users u ON u.id = p.user_id
        LEFT JOIN follows f
            ON f.following_id = u.id
           AND f.follower_id = %s
        ORDER BY p.created_at DESC
    """, (me,))

    data = cur.fetchall()
    db.close()

    return jsonify(data)
