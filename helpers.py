import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

#error message to be displayed
def apology(message, code=400):
    """Render message as an apology to user."""

    return render_template("apology.html", top=code, bottom=(message)), code

#require login
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("account_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
