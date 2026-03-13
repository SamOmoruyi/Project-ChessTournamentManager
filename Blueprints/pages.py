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
    tournamentID = session["currentTournament"]
    tournamentID = int(tournamentID[0])
    tournamentDetails = db.fetchTournament(tournamentID)
    tournamentSize = tournamentDetails[0][3]
    return render_template("tournamentplayerselection.html", db = db, tournamentSize = tournamentSize, tournamentID = tournamentID)

@pages.route("/bracketview/<tournamentID>")
def onView(tournamentID):
    #fetching data info + ensuring it is correct no matter where you view from
    tournamentID = int(tournamentID)
    currentTournament = tournamentID
    session["currentTournament"] = currentTournament
    db = DataBaseHandler()
    #fetching the rest of details for this tournament
    tournamentDetails = db.fetchTournament(tournamentID)
    tournamentSize = tournamentDetails[0][3]
    #fetching matchIDs
    matchIDs = db.fetchAllMatchIDs(tournamentID)
    #creating bracket
    bracket = []
    numberOfRounds = int(math.log2(tournamentSize))
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
    #placing all the matches for each round
    for i in range(0, (int(tournamentSize) - 1)):
        topAndBotIDs = db.fetchTopandBotIDs(matchIDs[i][0])
        playerNames = []
        if topAndBotIDs[0][0] != None: 
            playerNames.append(db.fetchPlayerName(topAndBotIDs[0][0]))
        if topAndBotIDs[0][1] != None:
            playerNames.append(db.fetchPlayerName(topAndBotIDs[0][1]))
        if i == 0:
            final.append(playerNames)
        elif i < 3:
            semiFinal.append(playerNames)
        elif i < 7:
            quarterFinal.append(playerNames)
        else:
                roundOf16.append(playerNames)
    session["bracket"] = bracket
    print(bracket)
    print(bracket[0])
    print(bracket[0][0])
    print(bracket[0][0][0])
    print(bracket[0][0][0][0])
    return "hiiii"
    return render_template("tournamentbracketview.html", bracket = bracket, db = db, tournamentID = tournamentID, tournamentSize = tournamentSize)

@pages.route("/updatetournament")
def onUpdate():
    #fetching bracket as well as extra info:
    bracket = session["bracket"]
    tournamentID = session["tournamentID"]
    currentUser = session["currentUser"]
    #ensuring all data from database is collected in the correct format
    currentUser = str(currentUser)
    db = DataBaseHandler()
    tournamentDetails = db.fetchTournament(tournamentID)
    tournamentOwner = tournamentDetails[0][1]
    tournamentOwner = str(tournamentOwner)
    #validation to prevent users who are not the owner from being able to update tournament
    if currentUser != tournamentOwner:
        return redirect(url_for("pages.onView", tournamentID = tournamentID))
    return render_template("tournamentupdating.html", bracket = bracket, tournamentID = tournamentID)