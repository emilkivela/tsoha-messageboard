from app import app
from flask import render_template, redirect, session, request, url_for
import threads, messages, users

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
		if users.login(username, password):
			return redirect("/")
		else:
			return render_template("error.html", error="Väärä käyttäjänimi tai salasana")
		

@app.route("/signin", methods=["POST", "GET"])
def signin():
	if request.method == "GET":
		return render_template("signin.html")
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		if users.signin(username, password):
			return redirect("/login")
		else:
			return render_template("error.html", error="Kirjautuminen ei onnistunut")

@app.route("/logout")
def logout():
	users.logout()
	return redirect("/")

@app.route("/new")
def new():
	if not session.get("user_id"):
		return redirect("/login")
	return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
	name = request.form["name"]
	op = session.get("user_id")
	threads.add_thread(name, op)
	return redirect("/")

@app.route("/thread/<int:id>", methods=["POST", "GET"])
def thread(id):
	if not session.get("user_id"):
		return redirect("/login")
	if request.method =="POST":
		user_id = session.get("user_id")
		message = request.form["message"]
		messages.add_message(message, id ,user_id)
		return redirect(url_for("thread", id=id))
	else:
		name = threads.get_name(id)
		list = messages.get_list(id)
		return render_template("thread.html", messages=list, name=name)

@app.route("/directs", methods=["POST", "GET"])
def directs():
	if not session.get("user_id"):
		return redirect("/login")
	user_id = session.get("user_id")
	if request.method == "POST":
		to = request.form["receiver"]
		message = request.form["content"]
		messages.direct_message(user_id, to, message)
		return redirect(url_for("directs"))
	else:
		received, sent = messages.get_directs(user_id)
		targets = users.get_users(user_id)
		return render_template("direct.html", users=targets, received=received, sent=sent)

