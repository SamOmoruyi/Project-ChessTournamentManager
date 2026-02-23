from flask import Blueprint, app, get_flashed_messages, redirect, render_template, session, url_for
from database import DataBaseHandler
from Scripts.isAuthorised import isAuthorised
import math
pages = Blueprint("pages", __name__)

# Dashboard page which has validation to prevent access for guest users 
@pages.route("/dashboard")
def dashboard():
    if not isAuthorised():
        return redirect(url_for("pages.guestdashboard"))
    currentUser = session["currentUser"] 
    userID = session.get("userID")
    db = DataBaseHandler()
    return render_template("dashboard.html", currentUser = currentUser, db = db, userID = userID)

# These 3 pages have validation to prevent you from accessing them if you are logged in
@pages.route("/")
def guestdashboard():
    if isAuthorised():
        return redirect(url_for("pages.dashboard"))
    return render_template("guestdashboard.html")

@pages.route("/login")
def login():
    if isAuthorised():
        return redirect(url_for("pages.dashboard"))
    return render_template("login.html")

@pages.route("/signup")
def signup():
    if isAuthorised():
        return redirect(url_for("pages.dashboard"))
    return render_template("signup.html")

@pages.route("/tournaments")
def tournamentHome():
    if not isAuthorised():
        return redirect(url_for("pages.login"))
    currentUser = session["currentUser"] 
    userID = session.get("userID")
    db = DataBaseHandler()
    return render_template("tournamenthome.html", currentUser = currentUser, db = db, userID = userID)

@pages.route("/createtournament")
def createTournament():
    db = DataBaseHandler()
    return render_template("tournamentcreation.html")

@pages.route("/createplayers")
def createPlayers():
    db = DataBaseHandler()
    return render_template("tournamentplayerselection.html", db = db)

@pages.route("/bracketview")
def onView():
    tournamentSize = session["tournamentSize"]
    tournamentID = session["tournamentID"]
    db = DataBaseHandler()
    bracket = db.fetchAllMatchIDs()
    numberOfRounds = math.log2(tournamentSize)
    n = numberOfRounds
    temp = 1
    round = []
    while n != 0:
        bracket.append(round + str(n))
        n = n - 1
    n = numberOfRounds
    while temp <= numberOfRounds:
        while len(round + str(n)) < temp:
            for i in range(temp):
                (round + str(n)).append(bracket[i])

