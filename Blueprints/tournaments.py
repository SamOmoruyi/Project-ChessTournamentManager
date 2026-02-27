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
    print(str(session["tournamentID"]))
    if success:
        return redirect(url_for("pages.tournamentplayerselection"))
    if errorType == "integrity-error":
        flash("Invalid data has been entered - Please try again")
    elif errorType == "unique-error":
        flash("Tournament name taken - Please use a different username")
    else:
        flash("An error has occurred")
    return redirect(url_for("pages.createplayers"))

@tournaments.route("/createplayers", methods = ["POST"])
def createPlayers():
    db = DataBaseHandler()
    tournamentName = session["tournamentName"] 
    tournamentID = session["tournamentID"]
    tournamentSize = session["tournamentSize"]
    n = 1
    while n != tournamentSize - 1:
        formDetails = request.form
        playerName = formDetails.get("playerName")
        db.addPlayer(playerName, tournamentID)
        n = n + 1
    #bit that makes the matches
    while n != int(tournamentSize - 1):
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
    
    return redirect(url_for("pages.bracketview", tournamentID = tournamentID, tournamentSize = tournamentSize, tournamentName = tournamentName))
