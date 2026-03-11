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
    currentTournament = ""
    session["currentTournament"] = currentTournament
    print(currentTournament)
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
    tournaments = db.fetchTournaments()
    print(tournaments)
    print(tournaments[0])
    return render_template("tournamenthome.html", currentUser = currentUser, db = db, userID = userID, tournaments = tournaments)

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

@pages.route("/bracketview/<int:tournamentID>")
def onView(tournamentID):
    print(tournamentID)
    tournamentID = int(tournamentID)
    currentTournament = tournamentID
    session["currentTournament"] = currentTournament
    db = DataBaseHandler()
    tournamentDetails = db.fetchTournament(tournamentID)
    print(tournamentDetails)
    tournamentSize = tournamentDetails[788]
    print(tournamentID)
    matchIDs = db.fetchAllMatchIDs(tournamentID[0])
    print(matchIDs)
    bracket = []
    numberOfRounds = math.log2(tournamentSize)
    n = numberOfRounds
    while n != 0:
        if n == 1:
            final = []
            bracket.append(final)
            tournamentWinner = []
            bracket.append(tournamentWinner)
        if n == 2:
            semiFinal = []
            bracket.append(semiFinal)
        if n == 3:
            quarterFinal = []
            bracket.append(quarterFinal)
        if n == 4:
            roundOf16 = []
            bracket.append(roundOf16)
        n = n - 1
    n = numberOfRounds

    while n != 0 :
        if n == 1:
            final.append(matchIDs[0][0])
        if n == 2:
            semiFinal.append(matchIDs[1][0])
            semiFinal.append(matchIDs[2][0])
        if n == 3:
           quarterFinal.append(matchIDs[3][0])
           quarterFinal.append(matchIDs[4][0])
           quarterFinal.append(matchIDs[5][0])
           quarterFinal.append(matchIDs[6][0])
        if n == 4:
            roundOf16.append(matchIDs[7][0])
            roundOf16.append(matchIDs[8][0])
            roundOf16.append(matchIDs[9][0])
            roundOf16.append(matchIDs[10][0])
            roundOf16.append(matchIDs[11][0])
            roundOf16.append(matchIDs[12][0])
            roundOf16.append(matchIDs[13][0])
            roundOf16.append(matchIDs[14][0])
        n = n - 1
        
        for i in range(0, (int(tournamentSize) - 1)):
            print(i)
            print(matchIDs)
            topAndBotIDs = db.fetchTopandBotIDs(matchIDs[i][0])
            playerNames = []
            playerNames.append(db.fetchPlayerName(topAndBotIDs[0][0]))
            playerNames.append(db.fetchPlayerName(topAndBotIDs[0][1]))
            if i == 0:
                matchIDs = []
                matchIDs.append(playerNames)
                final.append(matchIDs)
            elif i < 3:
                matchIDs = []
                matchIDs.append(playerNames)
                semiFinal.append(matchIDs)
            elif i < 7:
                matchIDs = []
                matchIDs.append(playerNames)
                quarterFinal.append(matchIDs)
            else:
                roundOf16.append(playerNames)
            print(i)
            print(matchIDs)
            print(matchIDs[i])
    print(playerNames)
    print(final)
    print(matchIDs)
    print(bracket)
    session["bracket"] = bracket
    print(bracket[0])
    return "hiiii"
    return render_template("tournamentbracketview.html", bracket = bracket, db = db, tournamentID = tournamentID, tournamentSize = tournamentSize)

@pages.route("/updatetournament")
def onUpdate():
    bracket = session["bracket"]
    tournamentID = session["tournamentID"]
    return render_template("tournamentupdating.html", bracket = bracket, tournamentID = tournamentID)