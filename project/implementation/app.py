from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from matplotlib.figure import Figure
import base64
from io import BytesIO
import datetime

# Modeling after finance pset

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data.db")

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.context_processor
def remember_color():
    """Remember user's color scheme"""

    # set the color equal to the user's chosen color scheme
    if session.get("user_id") is not None:
        color = db.execute("SELECT theme FROM users WHERE id = ?", session["user_id"])[0]["theme"]
    
    # Use light theme if no user is logged in 
    else:
        color = "light"
    return dict(color=color)


@app.route("/")
def index():
    """Displays the home page"""

    # show the user's name if they are logged in
    if session.get("user_id") is not None:
        name = ", " + db.execute("SELECT name FROM users WHERE id = ?", session["user_id"])[0]["name"]
    else:
        name = ""
    
    return render_template("index.html", name=name)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # storing form data
    username = request.form.get("username")
    password = request.form.get("password")

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not username:
            return render_template("error.html", error="missing username!")

        # Ensure password was submitted
        elif not password:
            return render_template("error.html", error="missing password!")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return render_template("error.html", error="invalid login!")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    # storing form data
    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    theme = request.form.get("theme")

    # If user reached route using POST by submitting the form
    if request.method == "POST":
        # Ensure name was completed 
        if not name:
            return render_template("error.html", error="missing name!")
        
        # Ensure username was completed 
        if not username:
            return render_template("error.html", error="missing username!")

        # Ensure passwords were completed
        if not password or not confirmation:
            return render_template("error.html", error="missing password!")

        # Ensure password and confirmation match
        if not password == confirmation:
            return render_template("error.html", error="password and confirmation must match!")
        
        # Ensure username is not already taken
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        
        if len(rows) > 0:
            return render_template("error.html", error="username taken!")
        
        # Ensure color scheme is in the list
        if theme not in ['light', 'dark', 'pastel']:
            return render_template("error.html", error="invalid color theme")

        # Insert user into the users table
        hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        new_id = db.execute("INSERT INTO users (username, hash, name, theme) VALUES(?, ?, ?, ?)", username, hash, name, theme)

        # Log user in
        session["user_id"] = new_id
        return redirect("/")

    # If user reached route using GET method send them to the register page
    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/activities")
@login_required
def activities():
    """Displays activities"""

    # getting the dates of the last 7 days
    today = datetime.datetime.now()
    dates = []

    for i in range(7):
        delta = datetime.timedelta(days=(6-i))
        rawdate = str(today - delta)[:10]
        dates.append(rawdate)

    # Generating the sleep graph
    sleep_amounts = []

    for date in dates:
        amount = db.execute("SELECT AVG(amount) AS amount FROM sleep WHERE user_id = ? AND date = ?", session["user_id"], date)[0]['amount']
        if amount == None:
            amount = 0

        sleep_amounts.append(amount)

    fig = Figure()
    ax = fig.subplots()
    ax.bar(dates, sleep_amounts, color = "purple")
    ax.set_xlabel('Date')
    ax.set_ylabel('Hours')
    ax.set_title("Timeline: Last 7 Days")
    fig.autofmt_xdate()
    buf = BytesIO()
    fig.savefig(buf, format="png")
    sleep = base64.b64encode(buf.getbuffer()).decode("ascii")

    # generating water graph
    water_amounts = []

    for date in dates:
        amount = db.execute("SELECT AVG(amount) AS amount FROM water WHERE user_id = ? AND date = ?", session["user_id"], date)[0]['amount']
        if amount == None:
            amount = 0

        water_amounts.append(amount)

    fig = Figure()
    ax = fig.subplots()
    ax.bar(dates, water_amounts)
    ax.set_xlabel('Date')
    ax.set_ylabel('Liters')
    ax.set_title("Timeline: Last 7 Days")
    fig.autofmt_xdate()
    buf = BytesIO()
    fig.savefig(buf, format="png")
    water = base64.b64encode(buf.getbuffer()).decode("ascii")

    # generating exercise graph
    exercise_amounts = []

    for date in dates:
        amount = db.execute("SELECT AVG(amount) AS amount FROM exercise WHERE user_id = ? AND date = ?", session["user_id"], date)[0]['amount']
        if amount == None:
            amount = 0

        exercise_amounts.append(amount)

    fig = Figure()
    ax = fig.subplots()
    ax.bar(dates, exercise_amounts, color='red')
    ax.set_xlabel('Date')
    ax.set_ylabel('Minutes')
    ax.set_title("Timeline: Last 7 Days")
    fig.autofmt_xdate()
    buf = BytesIO()
    fig.savefig(buf, format="png")
    exercise = base64.b64encode(buf.getbuffer()).decode("ascii")

    # generating relaxation graph
    relax_amounts = []

    for date in dates:
        amount = db.execute("SELECT AVG(amount) AS amount FROM relaxation WHERE user_id = ? AND date = ?", session["user_id"], date)[0]['amount']
        if amount == None:
            amount = 0

        relax_amounts.append(amount)

    fig = Figure()
    ax = fig.subplots()
    ax.bar(dates, relax_amounts, color='green')
    ax.set_xlabel('Date')
    ax.set_ylabel('Minutes')
    ax.set_title("Timeline: Last 7 Days")
    fig.autofmt_xdate()
    buf = BytesIO()
    fig.savefig(buf, format="png")
    relax = base64.b64encode(buf.getbuffer()).decode("ascii")

    # render the activities template
    return render_template("activities.html", sleep=sleep, water=water, exercise=exercise, relax=relax)


@app.route("/sleep", methods=["POST"])
@login_required
def sleep():
    """Adds data into the sleep table"""

    # storing all form responses
    date = request.form.get("date")
    amount = request.form.get("amount")
    
    # error checking
    if not date:
        return render_template("error.html", error="missing date")

    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        isdate = True
    except:
        isdate = False

    if not isdate:
        return render_template("error.html", error="invalid date")
    
    if amount != "":
        try:
            float(amount)
            isfloat = True
        except:
            isfloat = False
        
        if not isfloat:
            return render_template("error.html", error="invalid amount")

        if float(amount) < 0:
            return render_template("error.html", error="invalid amount")

    # Update/insert amount value
    current_dates = db.execute("SELECT date FROM sleep WHERE user_id = ?", session["user_id"])
    if date in [dict["date"] for dict in current_dates]:
        if not amount:
            db.execute("DELETE FROM sleep WHERE user_id = ? AND date = ?", session["user_id"], date)
        else:
            db.execute("UPDATE sleep SET amount = ? WHERE user_id = ? AND date = ?", amount, session["user_id"], date)
    else:
        db.execute("INSERT INTO sleep (user_id, amount, date) VALUES(?, ?, ?)", session["user_id"], amount, date)
    
    return redirect("/activities")


@app.route("/water", methods=["POST"])
@login_required
def water():
    """Adds data into the water table"""

    # storing all form responses
    date = request.form.get("date")
    amount = request.form.get("amount")

    # error checking
    if not date:
        return render_template("error.html", error="missing date")

    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        isdate = True
    except:
        isdate = False

    if not isdate:
        return render_template("error.html", error="invalid date")
    
    if amount != "":
        try:
            float(amount)
            isfloat = True
        except:
            isfloat = False
        
        if not isfloat:
            return render_template("error.html", error="invalid amount")

        if float(amount) < 0:
            return render_template("error.html", error="invalid amount")
    
    # Update/insert amount value
    current_dates = db.execute("SELECT date FROM water WHERE user_id = ?", session["user_id"])
    if date in [dict["date"] for dict in current_dates]:
        if not amount:
            db.execute("DELETE FROM water WHERE user_id = ? AND date = ?", session["user_id"], date)
        else:
            db.execute("UPDATE water SET amount = ? WHERE user_id = ? AND date = ?", amount, session["user_id"], date)
    else:
        db.execute("INSERT INTO water (user_id, amount, date) VALUES(?, ?, ?)", session["user_id"], amount, date)
    
    return redirect("/activities")


@app.route("/exercise", methods=["POST"])
@login_required
def exercise():
    """Adds data into the exercise table"""

    # storing all form responses
    date = request.form.get("date")
    amount = request.form.get("amount")

    # error checking
    if not date:
        return render_template("error.html", error="missing date")

    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        isdate = True
    except:
        isdate = False

    if not isdate:
        return render_template("error.html", error="invalid date")
    
    if amount != "":
        try:
            float(amount)
            isfloat = True
        except:
            isfloat = False
        
        if not isfloat:
            return render_template("error.html", error="invalid amount")

        if float(amount) < 0:
            return render_template("error.html", error="invalid amount")
    
    # Update/insert amount value
    current_dates = db.execute("SELECT date FROM exercise WHERE user_id = ?", session["user_id"])
    if date in [dict["date"] for dict in current_dates]:
        if not amount:
            db.execute("DELETE FROM exercise WHERE user_id = ? AND date = ?", session["user_id"], date)
        else:
            db.execute("UPDATE exercise SET amount = ? WHERE user_id = ? AND date = ?", amount, session["user_id"], date)
    else:
        db.execute("INSERT INTO exercise (user_id, amount, date) VALUES(?, ?, ?)", session["user_id"], amount, date)

    return redirect("/activities")


@app.route("/relaxation", methods=["POST"])
@login_required
def relaxation():
    """Adds data into the relaxation table"""

    date = request.form.get("date")
    amount = request.form.get("amount")

    # error checking
    if not date:
        return render_template("error.html", error="missing date")

    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        isdate = True
    except:
        isdate = False

    if not isdate:
        return render_template("error.html", error="invalid date")
    
    if amount != "":
        try:
            float(amount)
            isfloat = True
        except:
            isfloat = False
        
        if not isfloat:
            return render_template("error.html", error="invalid amount")

        if float(amount) < 0:
            return render_template("error.html", error="invalid amount")

    # Update/insert amount value
    current_dates = db.execute("SELECT date FROM relaxation WHERE user_id = ?", session["user_id"])
    if date in [dict["date"] for dict in current_dates]:
        if not amount:
            db.execute("DELETE FROM relaxation WHERE user_id = ? AND date = ?", session["user_id"], date)
        else:
            db.execute("UPDATE relaxation SET amount = ? WHERE user_id = ? AND date = ?", amount, session["user_id"], date)
    else:
        db.execute("INSERT INTO relaxation (user_id, amount, date) VALUES(?, ?, ?)", session["user_id"], amount, date)

    return redirect("/activities")


@app.route("/goals", methods=["GET", "POST"])
@login_required
def goals():
    """Displays goals"""

    # If using the post method, add the new goal into the database
    if request.method == "POST":
        if not request.form.get("addgoal"):
            return render_template("error.html", error="missing goal!")
        
        db.execute("INSERT INTO goals (user_id, goal) VALUES(?, ?)", session["user_id"], request.form.get("addgoal"))

        return redirect("/goals")
    
    # Display the current goals as a complete list and an incomplete list
    else:
        completes = db.execute("SELECT id, goal FROM goals WHERE user_id = ? AND complete = ? AND deleted = ?", session["user_id"], 1, 0)
        incompletes = db.execute("SELECT id, goal FROM goals WHERE user_id = ? AND complete = ? AND deleted = ?", session["user_id"], 0, 0)
        
        return render_template("goals.html", completes=completes, incompletes=incompletes)


@app.route("/tocomplete/<id>")
@login_required
def tocomplete(id):
    """Changes a goal's completion status to complete"""

    # update SQL database and go back to goals page
    db.execute("UPDATE goals SET complete = ? WHERE id = ?", 1, id)
    
    return redirect("/goals")


@app.route("/toincomplete/<id>")
@login_required
def toincomplete(id):
    """changes a goal's completion status to incomplete"""

    # update SQL database and go back to goals page
    db.execute("UPDATE goals SET complete = ? WHERE id = ?", 0, id)

    return redirect("/goals")


@app.route("/deletegoal/<id>")
@login_required
def deletegoal(id):
    """ deletes a goal from the database """

    # update SQL database and go back to goals page
    db.execute("UPDATE goals SET deleted = ? WHERE id = ?", 1, id)

    return redirect("/goals")


@app.route("/analytics")
@login_required
def analytics():
    """Displays analytics page """

    # Goal analytics
    total = db.execute("SELECT COUNT(*) FROM goals WHERE user_id = ?", session["user_id"])[0]["COUNT(*)"]
    complete = db.execute("SELECT COUNT(*) FROM goals WHERE user_id = ? AND complete = ?", session["user_id"], 1)[0]["COUNT(*)"]

    # Pie chart of current goals
    current_total = db.execute("SELECT COUNT(*) FROM goals WHERE user_id = ? AND deleted = ?", session["user_id"], 0)[0]["COUNT(*)"]
    if current_total != 0:
        labels = 'Complete', 'Incomplete'
        current_complete = db.execute("SELECT COUNT(*) FROM goals WHERE user_id = ? AND deleted = ? AND complete = ?", session["user_id"], 0, 1)[0]["COUNT(*)"]
        current_incomplete = db.execute("SELECT COUNT(*) FROM goals WHERE user_id = ? AND deleted = ? AND complete = ?", session["user_id"], 0, 0)[0]["COUNT(*)"]
        sizes = [current_complete, current_incomplete]

        fig = Figure()
        ax = fig.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax.axis('equal')
        ax.set_title("Current Goal Completion Rate (excluding deleted goals)")
        buf = BytesIO()
        fig.savefig(buf, format="png")
        pie = base64.b64encode(buf.getbuffer()).decode("ascii")
    else:
        sizes = [1]
        fig = Figure()
        ax = fig.subplots()
        ax.pie(sizes)
        ax.set_title("No Current Goals")
        buf = BytesIO()
        fig.savefig(buf, format="png")
        pie = base64.b64encode(buf.getbuffer()).decode("ascii")

    # Activitiy Averages
    today = datetime.datetime.now()
    dates = []

    for i in range(7):
        delta = datetime.timedelta(days=(6-i))
        rawdate = str(today - delta)[:10]
        dates.append(rawdate)

    sleep_overall = db.execute("SELECT AVG(amount) AS average FROM sleep WHERE user_id=?", session["user_id"])[0]["average"]
    if sleep_overall != None:
        sleep_overall = round(sleep_overall,2)
    water_overall = db.execute("SELECT AVG(amount) AS average FROM water WHERE user_id=?", session["user_id"])[0]["average"]
    if water_overall != None:
        water_overall = round(water_overall,2)
    exercise_overall = db.execute("SELECT AVG(amount) AS average FROM exercise WHERE user_id=?", session["user_id"])[0]["average"]
    if exercise_overall != None:
        exercise_overall = round(exercise_overall,2)
    relax_overall = db.execute("SELECT AVG(amount) AS average FROM relaxation WHERE user_id=?", session["user_id"])[0]["average"]
    if relax_overall != None:
        relax_overall = round(relax_overall,2)

    # Activity Histories
    sleep = db.execute("SELECT amount, date FROM sleep WHERE user_id=? ORDER BY date", session["user_id"])
    water = db.execute("SELECT amount, date FROM water WHERE user_id=? ORDER BY date", session["user_id"])
    exercise = db.execute("SELECT amount, date FROM exercise WHERE user_id=? ORDER BY date", session["user_id"])
    relax = db.execute("SELECT amount, date FROM relaxation WHERE user_id=? ORDER BY date", session["user_id"])

    return render_template("analytics.html", total=total, complete=complete, pie=pie, 
                            sleep_overall=sleep_overall, water_overall=water_overall, 
                            exercise_overall=exercise_overall, relax_overall=relax_overall, 
                            sleep=sleep, water=water, exercise=exercise, relax=relax)


@app.route("/recommendations")
@login_required
def recommend():
    """ displays the recommendation page """

    return render_template("recommendations.html")


@app.route("/account", methods=["GET"])
@login_required
def account():
    """ displays the account settings page """

    # get current username and theme
    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    theme = db.execute("SELECT theme FROM users WHERE id = ?", session["user_id"])[0]["theme"]
    
    # return the account template
    return render_template("account.html", username=username, theme=theme)


@app.route("/username", methods=["POST"])
@login_required
def username():
    """ Changes the account's username """

    # Storing variables from the form
    new_username = request.form.get("new_username")

    # Ensures new username was provided
    if not new_username:
        return render_template("error.html", error="no username provided!")

    # update username and return to the account page
    db.execute("UPDATE users SET username = ? WHERE id = ?", new_username, session["user_id"])
    
    return redirect("/account")


@app.route("/password", methods=["POST"])
@login_required
def password():
    """ Changes the account's password"""

    # Storing variables from the form
    new_password = request.form.get("new_password")
    current_password = request.form.get("current_password")
    confirm_password = request.form.get("confirm_password")

    # Ensures all fields were provided

    if not new_password or not current_password or not confirm_password:
        return render_template("error.html", error="password field missing!")

    # Ensures current password is correct
    current = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])
    if not check_password_hash(current[0]["hash"], current_password):
        return render_template("error.html", error="incorrect password!")

    # Ensures new password and confirmation match
    if new_password != confirm_password:
        return render_template("error.html", error="passwords do not match!")

    # update hashed password and log user out
    hash = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=8)
    db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, session["user_id"])

    # log user out 
    return redirect("/logout")


@app.route("/color", methods=["POST"])
@login_required
def color():
    """ Changes the account's color scheme """
    theme = request.form.get("theme")

    # Ensure color scheme is in the list
    if theme not in ['light', 'dark', 'pastel']:
        return render_template("error.html", error="invalid color theme")

    # update database and return to account page
    db.execute("UPDATE users SET theme = ? WHERE id = ?", theme, session["user_id"])
    
    return redirect("/account")