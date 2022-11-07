from flask import Flask 
from flask import render_template, redirect, request, session
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes




