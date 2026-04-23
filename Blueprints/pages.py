from flask import Blueprint, app, flash, get_flashed_messages, redirect, render_template, session, url_for
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
    currentTournament = None
    currentTournamentsMatchIDs = None
    session["currentTournament"] = currentTournament
    session["currentTournamentsMatchIDs"] = currentTournamentsMatchIDs
    db = DataBaseHandler()
    tournaments = db.fetchTournamentsByUser(userID)
    return render_template("dashboard.html", currentUser = currentUser, db = db, userID = userID, tournaments = tournaments)

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
    tournamentDetails = db.fetchTournament(tournamentID)
    tournamentSize = tournamentDetails[0][2]
    return render_template("tournamentplayerselection.html", db = db, tournamentSize = tournamentSize, tournamentID = tournamentID)

#Helper function to make proccess easier to see and approach
def groupMatches(matchData):
    groupedMatches = {}
    #create dictionary per round inside grouped matches dictionary
    for match in matchData:
        roundNumber = match[4]
        groupedMatches[roundNumber] = {}
    #creating a list
    for match in matchData:
        roundNumber = match[4]
        matchNumber = match[2]
        #creation of a mini array with the 2 players in each match
        groupedMatches[roundNumber][matchNumber] = []
    for match in matchData:
        #adding names and ids of each player
        roundNumber = match[4]
        matchNumber = match[2]
        playerName = match[0]
        playerID = match[1]

        if playerID == match[3]: #gives true of false based on if playerID matches winnerID
            isWinner = True
        else:
            isWinner = False
        
        matchPlayed = match[3] != None
        groupedMatches[roundNumber][matchNumber].append(
                {
                "matchID" : matchNumber,
                "playerName" : playerName,
                "playerID" : playerID,
                "isWinner" : isWinner,
                "matchPlayed" : matchPlayed
                }
            )
    return groupedMatches

@pages.route("/tournaments/<tournamentID>")
def onView(tournamentID):
    #blocking guests from entry
    if not isAuthorised():
        return redirect(url_for("pages.login"))
    #fetching data info + ensuring it is correct no matter where you view from
    tournamentID = int(tournamentID)
    currentTournament = tournamentID
    session["currentTournament"] = currentTournament
    db = DataBaseHandler()
    tournament = db.fetchTournament(tournamentID)
    tournamentName = tournament[0][1]
    matchDetails = db.getAllMatchDetails(tournamentID)
    groupedMatches = groupMatches(matchDetails) #from helper function
    return render_template("tournamentbracketview.html", matchDetails = matchDetails, tournamentID = currentTournament, matches = groupedMatches, tournamentName = tournamentName )