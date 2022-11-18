from app import app
from db import db
from flask import render_template, redirect, session, request
from werkzeug.security import check_password_hash, generate_password_hash
import threads

@app.route("/")
def index():
	if not session.get("user_id"):
		return redirect("/login")
	list = threads.get_list()

	return render_template("index.html", threads=list)

@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "GET":
		return render_template("login.html")
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		sql = "SELECT id, password FROM Users WHERE username=:username"
		result = db.session.execute(sql, {"username":username})
		user = result.fetchone()
		if not user:
			return render_template("error.html", error="Väärä käyttäjänimi")
		else:
			hash_value = user.password
			if check_password_hash(hash_value, password):
				session["user_id"] = user.id
				return redirect("/")
			else:
				return render_template("error.html", error="Väärä salasana")

@app.route("/signin", methods=["POST", "GET"])
def signin():
	if request.method == "GET":
		return render_template("signin.html")
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		sql = "SELECT id, password FROM Users WHERE username=:username"
		result = db.session.execute(sql, {"username":username})
		user = result.fetchone()
		if user:
			return render_template("error.html", error="Käyttäjänimi on jo käytössä.")
		hash_value = generate_password_hash(password)
		sql = "INSERT INTO Users (username, password, admin) VALUES (:username, :password, :admin)"
		db.session.execute(sql, {"username":username, "password":hash_value, "admin":"FALSE"})
		db.session.commit()
		return redirect("/login")

@app.route("/logout")
def logout():
	del session["user_id"]
	return redirect("/")

@app.route("/new")
def new():
	return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
	name = request.form["name"]
	op = session.get("user_id")
	sql = "INSERT INTO threads (name, op) values (:name, :op)"
	db.session.execute(sql, {"name": name, "op" : op})
	db.session.commit()
	return redirect("/")
