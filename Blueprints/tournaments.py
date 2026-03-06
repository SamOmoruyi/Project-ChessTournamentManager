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
    n = 1
    formData = request.form.items()

    print(formData)

    for player in formData:
        playerName = player[1]
        print(playerName)
        ##send this to the DB!
        db.addPlayer(playerName, tournamentID)
#bit that makes the first round of matches
    while n != int(tournamentSize - 1):
        print(tournamentID)
        db.createMatches(tournamentID)
        n = n + 1
    numberOfrounds = math.log2(tournamentSize)    
    n = numberOfrounds
    matchIDs = db.fetchAllMatchIDs(tournamentID)
    playerIDs = db.fetchAllPlayerIDs(tournamentID)
    if n == 1:
        db.updateTopID(playerIDs[0], matchIDs[0])
        db.updateBotID(playerIDs[1], matchIDs[0])
    if n == 2:
        db.updateTopID(playerIDs[0], matchIDs[0])
        db.updateBotID(playerIDs[1], matchIDs[0])
        db.updateTopID(playerIDs[2], matchIDs[1])
        db.updateBotID(playerIDs[3], matchIDs[1])
    if n == 3:
        db.updateTopID(playerIDs[0], matchIDs[0])
        db.updateBotID(playerIDs[1], matchIDs[0])
        db.updateTopID(playerIDs[2], matchIDs[1])
        db.updateBotID(playerIDs[3], matchIDs[1])
        db.updateTopID(playerIDs[4], matchIDs[2])
        db.updateBotID(playerIDs[5], matchIDs[2])
        db.updateTopID(playerIDs[6], matchIDs[3])
        db.updateBotID(playerIDs[7], matchIDs[3])
    if n == 4:
        db.updateTopID(playerIDs[0], matchIDs[0])
        db.updateBotID(playerIDs[1], matchIDs[0])
        db.updateTopID(playerIDs[2], matchIDs[1])
        db.updateBotID(playerIDs[3], matchIDs[1])
        db.updateTopID(playerIDs[4], matchIDs[2])
        db.updateBotID(playerIDs[5], matchIDs[2])
        db.updateTopID(playerIDs[6], matchIDs[3])
        db.updateBotID(playerIDs[7], matchIDs[3])
        db.updateTopID(playerIDs[8], matchIDs[4])
        db.updateBotID(playerIDs[9], matchIDs[4])
        db.updateTopID(playerIDs[10], matchIDs[5])
        db.updateBotID(playerIDs[11], matchIDs[5])
        db.updateTopID(playerIDs[12], matchIDs[6])
        db.updateBotID(playerIDs[13], matchIDs[6])
        db.updateTopID(playerIDs[14], matchIDs[7])
        db.updateBotID(playerIDs[15], matchIDs[7])

    return "Hello"
    
    return redirect(url_for("pages.bracketview", tournamentID = tournamentID, tournamentSize = tournamentSize, tournamentName = tournamentName))

@tournaments.route("/updatetournament", methods = ["POST"])
def updateTournament():
    formDetails = request.form
    winner = formDetails.get("winner")
    roundNumber = formDetails.get("roundnumber")
    int(roundNumber) == int(roundNumber) - 1
    if int(roundNumber) < 0:
        flash("Round number is invalid - Please try again.")
        return redirect(url_for("pages.updatetournament"))
    
    elif int(roundNumber) > 3:
        flash("Round number is invalid - Please try again.")
        return redirect(url_for("pages.updatetournament"))
    
    else:
        db = DataBaseHandler()
        tournamentID = session["tournamentID"]
        if db.fetchWinner(winner, tournamentID) == "":
            matchIDs = db.fetchAllMatchIDs()
            if roundNumber == 0:
                matchID = db.fetchWinnersMatchID()
                n = bracket[0].index(matchID)
                if n == 0:
                    db.updateTopID(tournamentID, winner, matchIDs[3])
                    return redirect(url_for("pages.bracketview"))
                elif n == 1:
                    db.updateBotID(tournamentID, winner, matchIDs[3])
                    return redirect(url_for("pages.bracketview"))
                elif n == 2:
                    db.updateTopID(tournamentID, winner, matchIDs[4])
                    return redirect(url_for("pages.bracketview"))
                elif n == 3:
                    db.updateBotID(tournamentID, winner, matchIDs[4])
                    return redirect(url_for("pages.bracketview"))
                elif n == 4:
                    db.updateTopID(tournamentID, winner, matchIDs[5])
                    return redirect(url_for("pages.bracketview"))
                elif n == 5:
                    db.updateBotID(tournamentID, winner, matchIDs[5])
                    return redirect(url_for("pages.bracketview"))
                elif n == 6:
                    db.updateTopID(tournamentID, winner, matchIDs[6])
                    return redirect(url_for("pages.bracketview"))
                elif n == 7:
                    db.updateBotID(tournamentID, winner, matchIDs[6])
                    return redirect(url_for("pages.bracketview"))
            elif roundNumber == 1:
                matchID = db.fetchWinnersMatchID()
                n = bracket[1].index(matchID)
                if n == 0:
                    db.updateTopID(tournamentID, winner, matchIDs[1])
                    return redirect(url_for("pages.bracketview"))
                elif n == 1:
                    db.updateBotID(tournamentID, winner, matchIDs[1])
                    return redirect(url_for("pages.bracketview"))
                elif n == 2:
                    db.updateTopID(tournamentID, winner, matchIDs[2])
                    return redirect(url_for("pages.bracketview"))
                elif n == 3:
                    db.updateBotID(tournamentID, winner, matchIDs[2])
                    return redirect(url_for("pages.bracketview"))
            elif roundNumber == 2:
                matchID = db.fetchWinnersMatchID()
                n = bracket[2].index(matchID)
                if n == 0:
                    db.updateTopID(tournamentID, winner, matchIDs[0])
                    return redirect(url_for("pages.bracketview"))
                elif n == 1:
                    db.updateBotID(tournamentID, winner, matchIDs[0])
                    return redirect(url_for("pages.bracketview"))
            elif roundNumber == 3:
                matchID = matchIDs[0]
                db.updateWinner(tournamentID, winner, matchID)
                bracket = session["bracket"]
                bracket[4] = winner
                flash(str(winner) + "has won the tournament!")
                return redirect(url_for("pages.bracketview"))
        else:
            flash("Match already has a winner - Please try again.")
            return redirect(url_for("pages.updatetournament"))