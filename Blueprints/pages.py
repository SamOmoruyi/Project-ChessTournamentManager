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
    userID = session["userID"]
    db = DataBaseHandler()
    print(currentUser)
    print(userID)
    print(session)
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
    userID = session["userID"]
    db = DataBaseHandler()
    return render_template("tournamenthome.html", currentUser = currentUser, db = db, userID = userID)

@pages.route("/createtournament")
def createTournament():
    if not isAuthorised():
        return redirect(url_for("pages.login"))
    currentUser = session["currentUser"] 
    userID = session["userID"]
    db = DataBaseHandler()
    return render_template("tournamentcreation.html", currentUser = currentUser, db = db, userID = userID)

@pages.route("/createplayers")
def createPlayers():
    if not isAuthorised():
        return redirect(url_for("pages.login"))
    db = DataBaseHandler()
    tournamentID = session["tournamentID"]
    tournamentSize = session["tournamentSize"]
    return render_template("tournamentplayerselection.html", db = db, tournamentSize = tournamentSize, tournamentID = tournamentID)

@pages.route("/bracketview")
def onView():
    tournamentSize = session["tournamentSize"]
    tournamentID = session["tournamentID"]
    db = DataBaseHandler()
    matchIDs = db.fetchAllMatchIDs(tournamentID)
    bracket = []
    numberOfRounds = math.log2(tournamentSize)
    n = numberOfRounds
    round = []
    while n != 0:
        if n == 1:
            final = round
            bracket.append(final)
        if n == 2:
            semiFinal = round
            bracket.append(semiFinal)
        if n == 3:
            quarterFinal = round
            bracket.append(quarterFinal)
        if n == 4:
            roundOf16 = round
            bracket.append(roundOf16)
        n = n - 1
    n = numberOfRounds
    while n != 0 :
        if n == 1:
            final.append(matchIDs[0])
        if n == 2:
            semiFinal.append(matchIDs[1])
            semiFinal.append(matchIDs[2])
        if n == 3:
           quarterFinal.append(matchIDs[3])
           quarterFinal.append(matchIDs[4])
           quarterFinal.append(matchIDs[5])
           quarterFinal.append(matchIDs[6])
        if n == 4:
            roundOf16.append(matchIDs[7])
            roundOf16.append(matchIDs[8])
            roundOf16.append(matchIDs[9])
            roundOf16.append(matchIDs[10])
            roundOf16.append(matchIDs[11])
            roundOf16.append(matchIDs[12])
            roundOf16.append(matchIDs[13])
            roundOf16.append(matchIDs[14])
        n = n - 1
        print(bracket)
        bracket = session["bracket"]
    return render_template("tournamentbracketview", bracket = bracket, db = db, tournamentID = tournamentID)