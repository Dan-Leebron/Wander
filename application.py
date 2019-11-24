import os
import time

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
from datetime import time
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    symbols = db.execute("SELECT DISTINCT symbol FROM transactions WHERE userid = :iden", iden = session["user_id"])
    counts = len(symbols)
    symlist = []
    for i in range(counts):
        symlist.append(symbols[i]["symbol"])
    print(symlist)
    cash = db.execute("SELECT cash FROM users WHERE id = :iden", iden = session["user_id"])
    sharenum = []
    for j in range(len(symlist)):
        placehold = db.execute("SELECT SUM(shares) FROM transactions WHERE symbol = :syms AND userid = :iden AND buysell = 'buy' GROUP BY symbol", syms = symlist[j], iden = session["user_id"])
        print(placehold[0]["SUM(shares)"])
        sells =  db.execute("SELECT SUM(shares) FROM transactions WHERE symbol = :syms AND userid = :iden AND buysell = 'sell' GROUP BY symbol", syms = symlist[j], iden = session["user_id"])
        if len(sells) == 0:
            sharenum.append(placehold[0]["SUM(shares)"])
            print("AAAA")
        else:
            print(sells[0]["SUM(shares)"])
            sharenum.append(int(placehold[0]["SUM(shares)"]) - int(sells[0]["SUM(shares)"]))
    currentp = []
    for k in range(len(symlist)):
        currentp.append(lookup(symlist[k])["price"])
    print(currentp)
    total = 0
    totalval =[]
    for l in range(len(symlist)):
        totalval.append(sharenum[l]*currentp[l])
        total += totalval[l]
    print(totalval)
    total += cash[0]["cash"]

    total = "{0:.2f}".format(total)
    for i in range(len(symlist)):
        symlist[i] = symlist[i].upper()


    return render_template("index.html", symlist = symlist, sharenum = sharenum, currentp = currentp, totalval = totalval,cash = "{0:.2f}".format(cash[0]["cash"]), total = total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        #return apology("trying to buy?", 420)

        if not request.form.get("symbol"):
            return apology("Must provide ticker", 403)
        if not request.form.get("shares"):
            return apology("Need number of shares", 403)

        sharenumber = request.form.get("shares")

        try:
            sharenumber = int(sharenumber)
        except ValueError:
            return apology("Enter an integer number of shares", 403)
            #return apology("Enter an integer number of shares", 403)

        if sharenumber < 1:
            return apology("Enter an integer above 0", 403)

        symbol = request.form.get("symbol")
        quotes = lookup(symbol)
        if not quotes:
            return apology("Invalid symbol", 403)

        totalprice = quotes["price"] * sharenumber

        availablecash = db.execute("SELECT cash FROM users WHERE id = :iden", iden = session["user_id"])
        availablecash = availablecash[0]["cash"]

        if availablecash < totalprice:
            return apology("Insufficient funds for purchase", 403)
        db.execute("INSERT INTO transactions (symbol, shares, price, buysell, timedate, userid) VALUES(:symbol,:snmb,:pri,:let,:tim,:idd)", symbol = symbol, snmb = sharenumber, pri = quotes["price"], let = "buy",
        tim = datetime.now(), idd = session["user_id"])

        db.execute("UPDATE users SET cash = cash - :totalprice WHERE id = :idd", totalprice = totalprice, idd = session["user_id"])
        return redirect("/")
    else:
        return render_template("buy.html")
    """Buy shares of stock"""
    #return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM transactions WHERE userid = :idd", idd = session["user_id"])
    counts = range(len(transactions))
    tsymbol = []
    tsharenum = []
    tprice = []
    tbuysell = []
    ttime = []
    for i in counts:
        tsymbol.append(transactions[i]['symbol'].upper())
        tsharenum.append(transactions[i]['shares'])
        tprice.append(transactions[i]['price'])
        tbuysell.append(transactions[i]['buysell'])
        ttime.append(transactions[i]['timedate'])
    return render_template("history.html", tsymbol = tsymbol, tsharenum = tsharenum, tprice = tprice, tbuysell = tbuysell, ttime = ttime)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide a symbol", 403)

        symbol = request.form.get("symbol")
        quotes = lookup(symbol)
        if not quotes:
            return apology("Need a valid symbol", 403)
        print(quotes["price"])
        return render_template("quoted.html", name = quotes["name"], price = quotes["price"], symbol = quotes["symbol"])


    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
         # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)


        elif not request.form.get("confirmation"):
            return apology("must verify password", 403)

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Password and re-entry must match", 403)

        if len(request.form.get("password")) < 2:
            return apology("Please have a password longer than 1 character...", 402)

        name = db.execute("SELECT username FROM users WHERE username = :username",
                          username=request.form.get("username"))

        if name:
            return apology("Username in use", 403)

        user = request.form.get("username")
        hashed = generate_password_hash(request.form.get("password"))


        db.execute("INSERT INTO users (username, hash) VALUES (:user,:hashed)", user = user, hashed = hashed)

        return render_template("login.html")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        symbols = db.execute("SELECT DISTINCT symbol FROM transactions WHERE userid = :iden AND buysell = 'buy'", iden = session["user_id"])
        counts = len(symbols)

        symlist = []
        for i in range(counts):
            symlist.append(symbols[i]["symbol"])

        if not request.form.get("symbol"):
            return apology("Must provide ticker", 403)
        if not request.form.get("shares"):
            return apology("Need number of shares", 403)
        if request.form.get('symbol') not in symlist:
            return apology("Enter a stock you have purchased")

        sharenumber = request.form.get("shares")
        totalbought = db.execute("SELECT SUM(shares) FROM transactions WHERE symbol = :sym AND buysell = 'buy' AND userid = :idd",
        sym = request.form.get("symbol").lower(), idd = session["user_id"])
        print(totalbought)
        totalsold = db.execute("SELECT SUM(shares) FROM transactions WHERE symbol = :sym AND buysell = 'sell' AND userid = :idd",
        sym = request.form.get("symbol").lower(), idd = session["user_id"])
        if totalsold[0]['SUM(shares)'] == None:
            totalsold[0]['SUM(shares)'] = 0
        print(totalsold)
        sharesowned = totalbought[0]['SUM(shares)'] - totalsold[0]['SUM(shares)']

        try:
            sharenumber = int(sharenumber)
        except ValueError:
            return apology("Enter an integer number of shares", 403)
            #return apology("Enter an integer number of shares", 403)

        if sharenumber < 1:
            return apology("Enter an integer above 0", 403)

        if int(sharenumber) > sharesowned:
            return apology("Trying to sell more stocks than owned", 403)

        symbol = request.form.get("symbol")
        quotes = lookup(symbol)

        totalprice = quotes["price"] * sharenumber

        db.execute("INSERT INTO transactions (symbol, shares, price, buysell, timedate, userid) VALUES(:sym,:sharenum,:pri,:lets,:now,:idd)", sym = symbol, sharenum = sharenumber, pri = quotes["price"], lets = "sell",
        now = datetime.now(), idd = session["user_id"])

        db.execute("UPDATE users SET cash = cash + :totalprice WHERE id = :idd", totalprice = totalprice, idd = session["user_id"])
        return redirect("/")
    else:
        return render_template("sell.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
