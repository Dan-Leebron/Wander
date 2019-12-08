import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, send_from_directory
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from helpers import apology, login_required

from datetime import datetime
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

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///wander.db")

@app.route("/")
@login_required
def profile():
    """Profile page"""
    #pulling user details from accounts database using session id as reference and loading them into the profile page
    db.execute("UPDATE accounts SET last_seen = ? WHERE id = ?", (datetime.now().date(), session["account_id"]))

    details = db.execute("SELECT name, gender, bio, hometown, last_seen, destination, email, id FROM accounts WHERE id = ?", session["account_id"])

    name=details[0]["name"]
    gender=details[0]["gender"]
    bio=details[0]["bio"]
    hometown=details[0]["hometown"]
    last_seen=details[0]["last_seen"]
    destination=details[0]["destination"]
    email=details[0]["email"]
    ID=details[0]["id"]

    #loading a dynamic number of interests into the profile page based on what the user submitted when they registered

    interests = db.execute("SELECT interests FROM interests2 WHERE id = ?", session["account_id"])

    intlist = []
    for i in range(len(interests)):
        intlist.append(interests[i]['interests'])
    print(intlist)

    lastint = (len(intlist))-1

    #actually loading the page and passing through the information
    return render_template("profile.html", name=name, gender=gender, bio=bio, hometown=hometown, last_seen=last_seen, interests=intlist, lastint=lastint, destination=destination, email=email, ID=ID)



# UPLOAD IMAGE
#setting the folder for profile pictures to the folder static and defining what extensions are allowed
UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#defining how to upload profile photos, accessed after registering an account but before showing the profile page
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):

            file.filename = str(session["account_id"]) + ".jpg"
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('uploaded_file', filename=filename))
            return redirect("/")

    return render_template("upload.html")

#redirecting the photo upload
@app.route("/upload", methods=["GET", "POST"])
#@login_required
def upload():
    if request.method == "POST":
         return redirect("/")
    else:
        return render_template("upload.html")




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
        rows = db.execute("SELECT * FROM accounts WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["account_id"] = rows[0]["id"]
        print(session["account_id"])
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
    #clearing users that the logging out user swiped through so you can iterate through them on the next login
    db.execute("DELETE FROM swiped")

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    session.clear()

    if request.method == "POST":
        #checking that certain fields are input and setting requirements on fields
        if not request.form.get("username"):
            return apology("You must enter a username.", 403)

        elif not request.form.get("password"):
            return apology("You must enter a password.", 403)

        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("Your passwords do not match.", 403)

        elif not any(char.isdigit() for char in request.form.get("password")):
            return apology("Password should contain at least one number.", 403)


        test_ = db.execute("SELECT COUNT(username) FROM accounts WHERE username = ?", request.form.get("username"))
        count_username = test_[0]["COUNT(username)"]

        if count_username > 0:
            return apology("Sorry, this username is already taken!", 403)

        hash = generate_password_hash(request.form.get("password"))
        newUser = db.execute("INSERT INTO accounts (name, dob, gender, hometown, username, password, destination, email, bio) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (request.form.get("name"), request.form.get("dob"), request.form.get("gender"), request.form.get("hometown"), request.form.get("username"), hash, request.form.get("destination"), request.form.get("email"), request.form.get("bio")))

        # for automatic login:
        session["account_id"] = newUser
        #getting list of interests
        lists = request.form.getlist('interests')
        print(lists)

        for x in range(len(lists)):
            db.execute("INSERT INTO interests2 (interests, id) VALUES (?, ?)", (lists[x], session["account_id"]))

        return redirect("/upload")

    else:
        return render_template("register.html")


@app.route("/match", methods=["GET", "POST"])
@login_required
def match():
    """Swipe through users"""

    if request.method == "POST":

        match = request.form.get("match")
        if match == "yes":
            #if the user wants to match with this profile, insert the user id and other profile id into matches
            #delete the other profile from the sql table swipee as we will load the next swipee when we go to the next page
            #record the other profile as being swiped through
            test_id = db.execute("SELECT id FROM swipee")
            s_id = test_id[0]["id"]
            db.execute("INSERT INTO matches (user_id, match_id) VALUES (:user_id, :match_id)", user_id = session["account_id"], match_id = s_id)

            db.execute("DELETE FROM swipee")
            db.execute("INSERT INTO swiped (swipedID) VALUES (?)", (s_id))
            return redirect("/match")
        else:
            #if the user does not want to match with this user, just insert their id into already swiped through and delete their info from the swipee table
            test_id = db.execute("SELECT id FROM swipee")
            s_id = test_id[0]["id"]
            db.execute("DELETE FROM swipee")
            db.execute("INSERT INTO swiped (swipedID) VALUES (?)", (s_id))
            return redirect("/match")

    #loading the first displayed user to match with
    #making sure there isn't any stored info from users swiped through previously
    db.execute("DELETE FROM swipee")

    #checking if you have looked through all the available users going to the same location and returning an apology if you have
    #if the count of users you have swiped through is equal to the amount of other users going, then you have gone through them all
    swiped_num = db.execute("SELECT COUNT(swipedID) FROM swiped")
    users_num = db.execute("SELECT COUNT(id) FROM accounts WHERE id != ? AND destination = (SELECT destination FROM accounts WHERE id = ?)", (session["account_id"]), (session["account_id"]))

    count_swiped = swiped_num[0]["COUNT(swipedID)"]
    count_users = users_num[0]["COUNT(id)"]


    if count_swiped == count_users:
        return apology("No users left to swipe through! Log out and back in to see them again.", 402)

    #getting the destination the user wants to visit
    dest_dict = db.execute("SELECT destination FROM accounts WHERE id = ?", (session["account_id"]))
    destination = dest_dict[0]["destination"]
    #getting the IDs of people the user already swiped through this session
    swipedID = db.execute("SELECT * FROM swiped")
    #pulling the information of a profile who wants to go to the same country as the user and that the user has not already swiped through
    swipee = db.execute("SELECT id, name, dob, destination, bio FROM accounts WHERE destination = :destination AND id != :session_id AND id NOT IN (SELECT * FROM swiped) ORDER BY RANDOM() LIMIT 1;", destination=destination, session_id=session["account_id"])

    swipee_id = swipee[0]["id"]
    name = swipee[0]["name"]
    #interests = swipee[0]["interests"]
    dob = swipee[0]["dob"]
    destination = swipee[0]["destination"]
    bio = swipee[0]["bio"]
    #inserting the information of the selected profile into the SQL table swipee which holds the information of the swipee until it is overwritten by the next profile loaded
    db.execute("INSERT INTO swipee (id, name, dob, destination, bio) VALUES (?, ?, ?, ?, ?)", (swipee_id), (name), (dob), (destination), (bio))
    print(swipee_id)
    return render_template("match.html", name=name, dob=dob, bio=bio, destination=destination, ID=swipee_id)


@app.route("/matches", methods=["GET", "POST"])
@login_required
def matches():
    """List of matches"""

    # query user's matches where user was choosing
    matches = db.execute("SELECT name FROM accounts WHERE id IN (SELECT match_id FROM matches WHERE user_id IN (SELECT id FROM accounts WHERE id = :account_id))", account_id = session["account_id"])
    # query user's matches where other profile was choosing
    matched = db.execute("SELECT name FROM accounts WHERE id IN (SELECT user_id FROM matches WHERE match_id IN (SELECT id FROM accounts WHERE id = :account_id))", account_id = session["account_id"])

    matched_count = range(len(matched))
    matches_count = range(len(matches))

    matched_names = []
    matches_names = []
    # iterate through these names and append to list
    for i in matched_count:
        matched_names.append(matched[i]["name"])
    for j in matches_count:
        matches_names.append(matches[j]["name"])

    # if name present in both lists then it is a match
    success = [value for value in matched_names if value in matches_names]

    # retrieve email of match
    emails = []
    for k in range(len(success)):
        email = db.execute("SELECT email FROM accounts WHERE name = ?", (success[k]))
        emails.append(email[0]["email"])

    # pass through match name and email to matches html page
    return render_template("matches.html", matches=success, emails=emails)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

# citations
# country dropdown for register.html: https://gist.github.com/danrovito/977bcb97c9c2dfd3398a
# flask for uploading profile photo: https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
# profile card for match.html: https://www.w3schools.com/howto/howto_css_profile_card.asp
# profile page layout for profile.html: https://www.w3schools.com/w3css/tryit.asp?filename=tryw3css_templates_cv&stacked=h