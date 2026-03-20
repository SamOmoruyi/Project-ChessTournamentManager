from database import DataBaseHandler
from flask import Blueprint, redirect, render_template, session, url_for, flash, request
import math

tournaments = Blueprint("tournaments",__name__,url_prefix="/tournaments")

@tournaments.route("/createtournament", methods = ["POST"])
def createTournament():
    #Grab details
    formDeatils = request.form
    tournamentName = formDeatils.get("tournamentName")
    tournamentDescription = formDeatils.get("tournamentDescription")
    tournamentDate = formDeatils.get("tournamentDate")
    tournamentSize = formDeatils.get("tournamentSize")
    tournamentSize = int(tournamentSize)
    errors = False
    #checking if details are valid 
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
    #opening database
    db = DataBaseHandler()
    #storing fetching session information
    username = session["currentUser"]
    userID = session["userID"]
    success, errorType, = db.addTournament(userID, tournamentName, username, tournamentDate, tournamentDescription, tournamentSize)
    session["currentTournament"] = db.fetchTournamentID(tournamentName)
    #sending user to next page
    if success:
        return redirect(url_for("pages.createPlayers"))
    #sending correct error message if errors occur
    if errorType == "integrity-error":
        flash("Invalid data has been entered - Please try again")
    elif errorType == "unique-error":
        flash("Tournament name taken - Please use a different username")
    else:
        flash("An error has occurred")
    return redirect(url_for("pages.createTournament"))

@tournaments.route("/createplayers", methods = ["POST"])
def createPlayers():
    #fetching session information
    tournamentID = session["currentTournament"]
    tournamentID = tournamentID[0]
    db = DataBaseHandler()
    tournamentDetails = db.fetchTournament(tournamentID)
    tournamentSize = tournamentDetails[0][3]
    tournamentName = tournamentDetails[0][0]
    n = 1
    #requesting form
    formData = request.form.items()
    #for loop that makes all the players requested one by one
    for player in formData:
        playerName = player[1]
        #send this to the DB!
        db.addPlayer(playerName, tournamentID)
    
    #bit that makes the first round of matches
    while n != int(tournamentSize):
        db.createMatches(tournamentID)
        n = n + 1
    #find out how many rounds there will be
    numberOfrounds = math.log2(tournamentSize)    
    n = numberOfrounds
    #fetch all required match and player IDs to create first round of matches
    matchIDs = db.fetchAllMatchIDs(tournamentID)
    playerIDs = db.fetchAllPlayerIDs(tournamentID)
    #determining where each user will start based on their ID and ammount of rounds 
    if n == 1:
        db.updateTopID(tournamentID, playerIDs[0][0], matchIDs[0][0])
        db.updateBotID(tournamentID, playerIDs[1][0], matchIDs[0][0])
    if n == 2:
        db.updateTopID(tournamentID, playerIDs[0][0], matchIDs[1][0])
        db.updateBotID(tournamentID, playerIDs[1][0], matchIDs[1][0])
        db.updateTopID(tournamentID, playerIDs[2][0], matchIDs[2][0])
        db.updateBotID(tournamentID, playerIDs[3][0], matchIDs[2][0])
    if n == 3:
        db.updateTopID(tournamentID, playerIDs[0][0], matchIDs[3][0])
        db.updateBotID(tournamentID, playerIDs[1][0], matchIDs[3][0])
        db.updateTopID(tournamentID, playerIDs[2][0], matchIDs[4][0])
        db.updateBotID(tournamentID, playerIDs[3][0], matchIDs[4][0])
        db.updateTopID(tournamentID, playerIDs[4][0], matchIDs[5][0])
        db.updateBotID(tournamentID, playerIDs[5][0], matchIDs[5][0])
        db.updateTopID(tournamentID, playerIDs[6][0], matchIDs[6][0])
        db.updateBotID(tournamentID, playerIDs[7][0], matchIDs[6][0])
    if n == 4:
        db.updateTopID(tournamentID, playerIDs[0][0], matchIDs[7][0])
        db.updateBotID(tournamentID, playerIDs[1][0], matchIDs[7][0])
        db.updateTopID(tournamentID, playerIDs[2][0], matchIDs[8][0])
        db.updateBotID(tournamentID, playerIDs[3][0], matchIDs[8][0])
        db.updateTopID(tournamentID, playerIDs[4][0], matchIDs[9][0])
        db.updateBotID(tournamentID, playerIDs[5][0], matchIDs[9][0])
        db.updateTopID(tournamentID, playerIDs[6][0], matchIDs[10][0])
        db.updateBotID(tournamentID, playerIDs[7][0], matchIDs[10][0])
        db.updateTopID(tournamentID, playerIDs[8][0], matchIDs[11][0])
        db.updateBotID(tournamentID, playerIDs[9][0], matchIDs[12][0])
        db.updateTopID(tournamentID, playerIDs[10][0], matchIDs[13][0])
        db.updateBotID(tournamentID, playerIDs[11][0], matchIDs[13][0])
        db.updateTopID(tournamentID, playerIDs[12][0], matchIDs[14][0])
        db.updateBotID(tournamentID, playerIDs[13][0], matchIDs[14][0])
        db.updateTopID(tournamentID, playerIDs[14][0], matchIDs[15][0])
        db.updateBotID(tournamentID, playerIDs[15][0], matchIDs[15][0])

    return redirect(url_for("pages.onView", tournamentID = tournamentID, tournamentSize = tournamentSize, tournamentName = tournamentName))


@tournaments.route("/updatematch", methods = ["POST"])
def updateMatch():
    formDetails = request.form
    print(formDetails)
    return formDetails

@tournaments.route("/updatetournament", methods = ["POST"])
def updateTournament():
    #fetch details
    db = DataBaseHandler()
    tournamentID = session["currentTournament"]
    tournamentDetails = db.fetchTournament(tournamentID)
    tournamentSize = tournamentDetails[0][3]
    formDetails = request.form
    winner = formDetails.get("winner")
    currentMatch = session["currentMatch"]
    #process to check if the winner is in that match
    topAndBotIDs = db.fetchTopandBotIDs(currentMatch)
    if None in topAndBotIDs:
        flash("Match does not have 2 players yet - Please try again")
        return redirect(url_for("pages.onUpdate"))
    playerNames = [] 
    playerNames.append(db.fetchPlayerName(topAndBotIDs[0][0]))
    playerNames.append(db.fetchPlayerName(topAndBotIDs[0][1]))
    print(playerNames)
    print(winner)
    if winner not in playerNames:
        flash("Winner selected is not in this match - Please try again")
        return redirect(url_for("pages.onUpdate", tournamentID = tournamentID, matchID = currentMatch))
    #ensures match does not have a winner
    if db.fetchWinner(winner, tournamentID) == None:
            matchIDs = db.fetchAllMatchIDs()
            bracket = session["bracket"]
            if tournamentSize == 2:
                roundNumber = 3
            elif tournamentSize == 4:
                semiFinal = bracket[0]
                if winner in semiFinal and db.fetchWinner(currentMatch) == None :
                    roundNumber = 2
                else:
                    roundNumber = 3
            elif tournamentSize == 8:
                semiFinal = bracket[1]
                quarterFinal = bracket[0]
                if winner in semiFinal and db.fetchWinner(currentMatch) == None :
                    roundNumber = 2
                elif winner in quarterFinal and db.fetchWinner(currentMatch) == None:
                    roundNumber = 1
                else:
                    roundNumber = 3
            elif tournamentSize == 16:
                roundOf16 = bracket[0]
                semiFinal = bracket[2]
                quarterFinal = bracket[1]
                if winner in semiFinal and db.fetchWinner(currentMatch) == None :
                    roundNumber = 2
                elif winner in quarterFinal and db.fetchWinner(currentMatch) == None:
                    roundNumber = 1
                elif winner in roundOf16 and db.fetchWinner(currentMatch) == None:
                    roundNumber = 0
                else:
                    roundNumber = 3
            #fetches where the player is relative to the tournament bracket
            if roundNumber == 0:
                matchID = db.fetchWinnersMatchID(winner, tournamentID)
                n = matchIDs.index(matchID)
                #validation for where the winner will go based on what round they came from and where they are in bracket
                if n == 7:
                    db.updateTopID(tournamentID, winner, matchIDs[3][0])
                    db.updateWinner(tournamentID, winner, matchIDs[7][0])
                    return redirect(url_for("pages.onView", tournamentID = tournamentID))
                elif n == 8:
                    db.updateBotID(tournamentID, winner, matchIDs[3][0])
                    db.updateWinner(tournamentID, winner, matchIDs[8][0])
                    return redirect(url_for("pages.onView", tournamentID = tournamentID))
                elif n == 9:
                    db.updateTopID(tournamentID, winner, matchIDs[4][0])
                    db.updateWinner(tournamentID, winner, matchIDs[9][0])
                    return redirect(url_for("pages.onView", tournamentID = tournamentID))
                elif n == 10:
                    db.updateBotID(tournamentID, winner, matchIDs[4][0])
                    db.updateWinner(tournamentID, winner, matchIDs[10][0])
                    return redirect(url_for("pages.onView", tournamentID = tournamentID))
                elif n == 11:
                    db.updateTopID(tournamentID, winner, matchIDs[5][0])
                    db.updateWinner(tournamentID, winner, matchIDs[11][0])
                    return redirect(url_for("pages.onView", tournamentID = tournamentID))
                elif n == 12:
                    db.updateBotID(tournamentID, winner, matchIDs[5][0])
                    db.updateWinner(tournamentID, winner, matchIDs[12][0])
                    return redirect(url_for("pages.onView", tournamentID = tournamentID))
                elif n == 13:
                    db.updateTopID(tournamentID, winner, matchIDs[6][0])
                    db.updateWinner(tournamentID, winner, matchIDs[13][0])
                    return redirect(url_for("pages.onView", tournamentID = tournamentID))
                elif n == 14:
                    db.updateBotID(tournamentID, winner, matchIDs[6][0])
                    db.updateWinner(tournamentID, winner, matchIDs[14][0])
                    return redirect(url_for("pages.onView", tournamentID = tournamentID))
            elif roundNumber == 1:
                matchID = db.fetchWinnersMatchID()
                n = matchIDs.index(matchID)
                if n == 3:
                    db.updateTopID(tournamentID, winner, matchIDs[1][0])
                    db.updateWinner(tournamentID, winner, matchIDs[3][0])
                    return redirect(url_for("pages.onView", tournamentID = tournamentID))
                elif n == 4:
                    db.updateBotID(tournamentID, winner, matchIDs[1][0])
                    db.updateWinner(tournamentID, winner, matchIDs[4][0])
                    return redirect(url_for("pages.onView", tournamentID = tournamentID))
                elif n == 5:
                    db.upd5ateTopID(tournamentID, winner, matchIDs[2][0])
                    db.updateWinner(tournamentID, winner, matchIDs[5][0])
                    return redirect(url_for("pages.onView", tournamentID = tournamentID))
                elif n == 6:
                    db.updateBotID(tournamentID, winner, matchIDs[2][0])
                    db.updateWinner(tournamentID, winner, matchIDs[6][0])
                    return redirect(url_for("pages.onView", tournamentID = tournamentID))
            elif roundNumber == 2:
                matchID = db.fetchWinnersMatchID()
                n = matchIDs.index(matchID)
                if n == 1:
                    db.updateTopID(tournamentID, winner, matchIDs[0][0])
                    db.updateWinner(tournamentID, winner, matchIDs[1][0])
                    return redirect(url_for("pages.onView", tournamentID = tournamentID))
                elif n == 2:
                    db.updateBotID(tournamentID, winner, matchIDs[0][0])
                    db.updateWinner(tournamentID, winner, matchIDs[2][0])
                    return redirect(url_for("pages.onView", tournamentID = tournamentID))
            #crowns winner of tournament
            elif roundNumber == 3:
                matchID = matchIDs[0][0]
                db.updateWinner(tournamentID, winner, matchID)
                bracket = session["bracket"]
                bracket[4] = winner
                flash(str(winner) + "has won the tournament!")
                return redirect(url_for("pages.onView", tournamentID = tournamentID))
    #result of check at the start
    else:
            flash("Match already has a winner - Please try again.")
            return redirect(url_for("pages.onUpdate"))