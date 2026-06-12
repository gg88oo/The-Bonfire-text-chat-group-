from flask import Flask, flash, redirect, render_template, request, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
import sqlite3
from cs50 import SQL

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQL("sqlite:///bonfire.db")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if session.get("user_id") is None:
            return redirect("/login")

        message = request.form.get("message")
        user_id = session["user_id"]
        username = db.execute("SELECT username FROM users WHERE user_id = ?", user_id) 
        username = username[0]["username"]
        db.execute("INSERT INTO messages (user_id, username, message) VALUES (?, ?, ?)", 
            user_id, username, message)
        return "", 204
    else:
        if session.get("user_id") is None:
            return redirect("/login")

        ##messages = db.execute("SELECT * FROM messages")
        return render_template("index.html")    

@app.route("/get_messages", methods=["POST", "GET"])  # Allow both methods
def get_messages():
    # Try to get last_id from POST first, then from GET
    last_id = request.form.get("last_id")
    if last_id is None:
        last_id = request.args.get("last_id", 0)
    
    last_id = int(last_id) if last_id else 0
    
    print(f"Getting messages with last_id > {last_id}")
    
    messages = db.execute("SELECT * FROM messages WHERE id > ?", last_id)
    print(f"Found {len(messages)} messages")
    
    return jsonify(messages)
    



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confrmation")  # Fixed typo

        if not username:
            return "username required"
        elif not password:
            return "password required"
        elif not confirmation:
            return "password again required"
        elif password != confirmation:
            return "passwords don't match"

            # Check if username exists
        check = db.execute("SELECT * FROM users WHERE username = ?", (username))
        print(check)
        if len(check) != 0:
            return "username aleardy exists"

                # Insert new user
        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", username, hash)
                # Get user_id
        user_id = db.execute("SELECT user_id FROM users WHERE username = ? ", (username))

        session["user_id"] = user_id[0]["user_id"]  # Assuming it returns a list of dicts
        return redirect("/")  # Or wherever you want to go

    else:
        return render_template("register.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()

    return redirect("/register")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = db.execute("SELECT user_id, password_hash FROM users WHERE username = ?", username)
        if user and check_password_hash(user[0]["password_hash"], password):
            session["user_id"] = user[0]["user_id"]
            return redirect("/")
        else:
            return "username or password wrong", 401
    elif request.method == "GET":
        return render_template("login.html")

        

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function
