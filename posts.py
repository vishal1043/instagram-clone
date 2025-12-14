from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_db
import os
from werkzeug.utils import secure_filename

# ✅ ONLY ONE Blueprint definition
posts = Blueprint("posts", __name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@posts.route("/api/post", methods=["POST"])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()

    image = request.files.get("image")
    caption = request.form.get("caption")

    if image:
        filename = secure_filename(image.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(path)
        image_url = f"/{path}"
    else:
        data = request.json
        image_url = data.get("image_url")
        caption = data.get("caption")

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO posts (user_id, image_url, caption) VALUES (%s,%s,%s)",
        (user_id, image_url, caption)
    )
    db.commit()
    db.close()

    return jsonify({"status": "success"})
