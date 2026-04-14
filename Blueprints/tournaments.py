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
    tournamentOwner = session["currentUser"]
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
    userID = session["userID"]
    success, errorType, = db.addTournament(userID, tournamentName, tournamentDate, tournamentDescription, tournamentSize)
    # print(errorType)
    # session["currentTournament"] = db.fetchTournamentID(tournamentName)
    #sending user to next page
    if success:
        session["currentTournament"] = errorType
        print(session.get("currentTournament"))
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
    db = DataBaseHandler()
    tournamentDetails = db.fetchTournament(tournamentID)
    tournamentSize = tournamentDetails[0][2]
    tournamentName = tournamentDetails[0][0]
    #requesting form
    formData = request.form.items()
    tournamentID = session.get("currentTournament")
    playerIDs = []
    numberOfrounds = int(math.log2(tournamentSize))
    #for loop that makes all the players requested one by one
    for player in formData:
        playerName = player[1]
        #send this to the DB!
        playerIDs.append(db.addPlayer(playerName, tournamentID))
    #for loop that makes the matchentries for round 1
    for i in range(0,len(playerIDs), 2):
        #make a match for each pairing - and return back the ID
        matchID = db.createMatches(tournamentID, 1)
        #then make a matchEntry for each player that will also incude the match ID and tournamentID
        db.createMatchEntry(matchID, playerIDs[i])
        db.createMatchEntry(matchID, playerIDs[i+1])
    n = int(0)  
    return redirect(url_for("pages.onView", tournamentID = tournamentID, tournamentSize = tournamentSize, tournamentName = tournamentName))
    return "done!"


@tournaments.route("/updatematch", methods = ["POST"])
def updateMatch():
    #opening database
    db = DataBaseHandler()
    #fetching form details
    formDetails = request.form
    tournamentID = formDetails.get("tournamentID")
    winner = formDetails.get("winner")
    matchID = formDetails.get("matchID")
    roundNumber = formDetails.get("roundNumber")
    print(formDetails)
    return formDetails
    #updating winner on the database
    db.updateWinner(tournamentID, winner, matchID)
    #check if all games with roundnumber winner is from have been played
        #if no do nothing else and return to bracketview
        #if yes checks if this is not the final round of the tournament
            #if no declare winner and return player to bracketview
            #if yes create all next round matches by fetching all winners from round
                #do this by pairing winners based on playerID where 2 smallest values pair up then the next and so on
                #then create match entries for each player based on these pairings
                #create a match after each entry is added 
@tournaments.route("/updatetournament", methods = ["POST"])
def updateTournament():
    #fetch details
    db = DataBaseHandler()
    tournamentID = session["currentTournament"]
    tournamentDetails = db.fetchTournament(tournamentID)
    tournamentSize = tournamentDetails[0][2]
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