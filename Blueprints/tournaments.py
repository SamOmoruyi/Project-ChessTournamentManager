from database import DataBaseHandler
from flask import Blueprint, redirect, render_template, session, url_for, flash, request
import math

tournaments = Blueprint("tournaments",__name__,url_prefix="/tournaments")

@tournaments.route("/createtournament", methods = ["POST"])
def createTournament():
    formDeatils = request.form
    tournamentName = formDeatils.get("tournamentName")
    tournamentDescription = formDeatils.get("tournamentDescription")
    tournamentDate = formDeatils.get("tournamentDate")
    tournamentSize = formDeatils.get("tournamentSize")
    tournamentSize = int(tournamentSize)
    errors = False
    possibleSizes = [2,4,8,16]
    if tournamentSize not in possibleSizes:
        flash("Tournaments can only have a size of 2, 4, 8 or 16 - Please try again.")
        errors = True

    if tournamentDescription == "":
        flash("Tournament must have a descripion - Please try again.")
        errors = True

    if tournamentName == "":
        flash("Tournament must have a name - Please try again.")
        errors = True
    
    if tournamentDate == "":
        flash("Tournament must have a date - Please try again.")
        errors = True
    
    if errors:
        return redirect(url_for("pages.createTournament"))
    db = DataBaseHandler()
    username = session["currentUser"]
    userID = session["userID"]
    success, errorType, = db.addTournament(userID, tournamentName, username, tournamentDate, tournamentDescription, tournamentSize)
    session["tournamentSize"] = tournamentSize
    session["tournamentName"] = tournamentName
    session["tournamentID"] = db.fetchTournamentID(tournamentName)
    if success:
        return redirect(url_for("pages.createPlayers"))
    if errorType == "integrity-error":
        flash("Invalid data has been entered - Please try again")
    elif errorType == "unique-error":
        flash("Tournament name taken - Please use a different username")
    else:
        flash("An error has occurred")
    return redirect(url_for("pages.createTournament"))

@tournaments.route("/createplayers", methods = ["POST"])
def createPlayers():
    db = DataBaseHandler()
    tournamentName = session["tournamentName"] 
    tournamentID = session["tournamentID"]
    tournamentSize = session["tournamentSize"]
    #bracket = session["bracket"]
    n = 1
    formData = request.form.items()
    for player in formData:
        playerName = player[1]
        ##send this to the DB!
        db.addPlayer(playerName, tournamentID[0])
    
#bit that makes the first round of matches
    while n != int(tournamentSize):
        db.createMatches(tournamentID[0])
        n = n + 1
    numberOfrounds = math.log2(tournamentSize)    
    n = numberOfrounds
    matchIDs = db.fetchAllMatchIDs(tournamentID[0])
    playerIDs = db.fetchAllPlayerIDs(tournamentID[0])
    if n == 1:
        db.updateTopID(tournamentID[0], playerIDs[0][0], matchIDs[0][0])
        db.updateBotID(tournamentID[0], playerIDs[1][0], matchIDs[0][0])
    if n == 2:
        db.updateTopID(tournamentID[0], playerIDs[0][0], matchIDs[1][0])
        db.updateBotID(tournamentID[0], playerIDs[1][0], matchIDs[1][0])
        db.updateTopID(tournamentID[0], playerIDs[2][0], matchIDs[2][0])
        db.updateBotID(tournamentID[0], playerIDs[3][0], matchIDs[2][0])
    if n == 3:
        db.updateTopID(tournamentID[0], playerIDs[0][0], matchIDs[3][0])
        db.updateBotID(tournamentID[0], playerIDs[1][0], matchIDs[3][0])
        db.updateTopID(tournamentID[0], playerIDs[2][0], matchIDs[4][0])
        db.updateBotID(tournamentID[0], playerIDs[3][0], matchIDs[4][0])
        db.updateTopID(tournamentID[0], playerIDs[4][0], matchIDs[5][0])
        db.updateBotID(tournamentID[0], playerIDs[5][0], matchIDs[5][0])
        db.updateTopID(tournamentID[0], playerIDs[6][0], matchIDs[6][0])
        db.updateBotID(tournamentID[0], playerIDs[7][0], matchIDs[6][0])
    if n == 4:
        db.updateTopID(tournamentID[0], playerIDs[0][0], matchIDs[7][0])
        db.updateBotID(tournamentID[0], playerIDs[1][0], matchIDs[7][0])
        db.updateTopID(tournamentID[0], playerIDs[2][0], matchIDs[8][0])
        db.updateBotID(tournamentID[0], playerIDs[3][0], matchIDs[8][0])
        db.updateTopID(tournamentID[0], playerIDs[4][0], matchIDs[9][0])
        db.updateBotID(tournamentID[0], playerIDs[5][0], matchIDs[9][0])
        db.updateTopID(tournamentID[0], playerIDs[6][0], matchIDs[10][0])
        db.updateBotID(tournamentID[0], playerIDs[7][0], matchIDs[10][0])
        db.updateTopID(tournamentID[0], playerIDs[8][0], matchIDs[11][0])
        db.updateBotID(tournamentID[0], playerIDs[9][0], matchIDs[12][0])
        db.updateTopID(tournamentID[0], playerIDs[10][0], matchIDs[13][0])
        db.updateBotID(tournamentID[0], playerIDs[11][0], matchIDs[13][0])
        db.updateTopID(tournamentID[0], playerIDs[12][0], matchIDs[14][0])
        db.updateBotID(tournamentID[0], playerIDs[13][0], matchIDs[14][0])
        db.updateTopID(tournamentID[0], playerIDs[14][0], matchIDs[15][0])
        db.updateBotID(tournamentID[0], playerIDs[15][0], matchIDs[15][0])

    return redirect(url_for("pages.onView", tournamentID = tournamentID, tournamentSize = tournamentSize, tournamentName = tournamentName))

@tournaments.route("/updatetournament", methods = ["POST"])
def updateTournament():
    formDetails = request.form
    winner = formDetails.get("winner")
    roundNumber = formDetails.get("roundnumber")
    int(roundNumber) == int(roundNumber) - 1
    if int(roundNumber) < 0:
        flash("Round number is invalid - Please try again.")
        return redirect(url_for("pages.onUpdate"))
    
    elif int(roundNumber) > 3:
        flash("Round number is invalid - Please try again.")
        return redirect(url_for("pages.onUpdate"))
    
    else:
        db = DataBaseHandler()
        tournamentID = session["tournamentID"]
        if db.fetchWinner(winner, tournamentID[0]) == "":
            matchIDs = db.fetchAllMatchIDs()
            if roundNumber == 0:
                matchID = db.fetchWinnersMatchID()
                n = bracket[0].index(matchID)
                if n == 0:
                    db.updateTopID(tournamentID[0], winner, matchIDs[3][0])
                    return redirect(url_for("pages.onView"))
                elif n == 1:
                    db.updateBotID(tournamentID[0], winner, matchIDs[3][0])
                    return redirect(url_for("pages.onView"))
                elif n == 2:
                    db.updateTopID(tournamentID[0], winner, matchIDs[4][0])
                    return redirect(url_for("pages.onView"))
                elif n == 3:
                    db.updateBotID(tournamentID[0], winner, matchIDs[4][0])
                    return redirect(url_for("pages.onView"))
                elif n == 4:
                    db.updateTopID(tournamentID[0], winner, matchIDs[5][0])
                    return redirect(url_for("pages.onView"))
                elif n == 5:
                    db.updateBotID(tournamentID[0], winner, matchIDs[5][0])
                    return redirect(url_for("pages.onView"))
                elif n == 6:
                    db.updateTopID(tournamentID[0], winner, matchIDs[6][0])
                    return redirect(url_for("pages.onView"))
                elif n == 7:
                    db.updateBotID(tournamentID[0], winner, matchIDs[6][0])
                    return redirect(url_for("pages.onView"))
            elif roundNumber == 1:
                matchID = db.fetchWinnersMatchID()
                n = bracket[1].index(matchID)
                if n == 0:
                    db.updateTopID(tournamentID[0], winner, matchIDs[1][0])
                    return redirect(url_for("pages.onView"))
                elif n == 1:
                    db.updateBotID(tournamentID[0], winner, matchIDs[1][0])
                    return redirect(url_for("pages.onView"))
                elif n == 2:
                    db.updateTopID(tournamentID[0], winner, matchIDs[2][0])
                    return redirect(url_for("pages.onView"))
                elif n == 3:
                    db.updateBotID(tournamentID[0], winner, matchIDs[2][0])
                    return redirect(url_for("pages.onView"))
            elif roundNumber == 2:
                matchID = db.fetchWinnersMatchID()
                n = bracket[2].index(matchID)
                if n == 0:
                    db.updateTopID(tournamentID[0], winner, matchIDs[0][0])
                    return redirect(url_for("pages.onView"))
                elif n == 1:
                    db.updateBotID(tournamentID[0], winner, matchIDs[0][0])
                    return redirect(url_for("pages.onView"))
            elif roundNumber == 3:
                matchID = matchIDs[0][0]
                db.updateWinner(tournamentID[0], winner, matchID)
                bracket = session["bracket"]
                bracket[4] = winner
                flash(str(winner) + "has won the tournament!")
                return redirect(url_for("pages.onView"))
        else:
            flash("Match already has a winner - Please try again.")
            return redirect(url_for("pages.onUpdate"))