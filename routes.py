from app import app
from flask import render_template, redirect, session, request, url_for
import threads, messages, users, topics

@app.route("/", methods=["POST", "GET"])
def index():
	if not session.get("user_id"):
		return redirect("/login")
	if request.method == "POST":
		topic_name = request.form["name"]
		user_id = session.get("user_id")
		topics.add_topic(topic_name, user_id)
		return redirect("/")
	else:
		list = topics.get_topics()
		return render_template("index.html", topics=list)

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

@app.route("/delete/thread<int:id>")
def delete_thread(id):
	user_id = session.get("user_id")
	if threads.check_permission(user_id, id):
		threads.delete_thread(id)
		return redirect("/")
	else:
		return render_template("error.html", error="Sinulle ei ole käyttöoikeutta tähän toimintoon")

@app.route("/delete/message<int:id>")
def delete_message(id):
	user_id = session.get("user_id")
	if messages.check_permission(user_id, id):
		messages.delete_message(id)
		return redirect("/")
	else:
		return render_template("error.html", error="Sinulle ei ole käyttöoikeutta tähän toimintoon")

@app.route("/topic/<int:id>", methods=["POST", "GET"])
def topic(id):
	if not session.get("user_id"):
		return redirect("/login")
	if request.method == "POST":
		creator = session.get("user_id")
		name = request.form["name"]
		threads.add_thread(name, creator, id)
		return redirect(url_for("topic", id=id))
	else:
		list = threads.get_list(id)
		name = topics.get_name(id)
		return render_template("topic.html", threads=list, name=name)

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

@app.route("/search<int:id>", methods=["GET"])
def search(id):
	if not session.get("user_id"):
		return redirect("/login")
	query = request.args["query"]
	list = messages.find_message(id, query)
	return render_template("search.html", messages=list)
