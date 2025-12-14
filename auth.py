from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt
from db import get_db

auth = Blueprint("auth", __name__)
@auth.route("/api/signup", methods=["POST"])
def signup():
    d = request.json

    db = get_db()
    cur = db.cursor()

    # ✅ CHECK username
    cur.execute("SELECT id FROM users WHERE username=%s", (d["username"],))
    if cur.fetchone():
        db.close()
        return jsonify({"msg": "Username already exists"}), 409

    # ✅ CHECK email
    cur.execute("SELECT id FROM users WHERE email=%s", (d["email"],))
    if cur.fetchone():
        db.close()
        return jsonify({"msg": "Email already exists"}), 409

    # ✅ HASH password
    hashed = bcrypt.hashpw(
        d["password"].encode(),
        bcrypt.gensalt()
    ).decode()

    # ✅ INSERT safely
    cur.execute(
        "INSERT INTO users(username, email, password) VALUES (%s, %s, %s)",
        (d["username"], d["email"], hashed)
    )

    db.commit()
    db.close()

    return jsonify({"msg": "signup_success"}), 201


@auth.route("/api/login", methods=["POST"])
def login():
    d = request.json
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT * FROM users WHERE email=%s", (d["email"],))
    user = cur.fetchone()
    db.close()

    if user and bcrypt.checkpw(d["password"].encode(), user["password"].encode()):
        token = create_access_token(identity=user["id"])
        return jsonify({
            "access_token": token,
            "user_id": user["id"],
            "username": user["username"]
        })

    return jsonify({"msg": "invalid credentials"}), 401
