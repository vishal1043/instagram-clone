from flask import Flask, render_template, redirect
from flask_jwt_extended import JWTManager

from auth import auth
from feed import feed
from posts import posts
from follow import follow
from likes import likes
from comments import comments
from search import search

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "secret123"
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
JWTManager(app)

app.register_blueprint(auth)
app.register_blueprint(feed)
app.register_blueprint(posts)
app.register_blueprint(follow)
app.register_blueprint(likes)
app.register_blueprint(comments)
app.register_blueprint(search)



@app.route("/")
def auth_page():
    return render_template("auth.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/create")
def create():
    return render_template("create_post.html")




if __name__ == "__main__":
    app.run(debug=True)
