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
    #sending user to next page
    if success:
        session["currentTournament"] = errorType
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
    tournamentID = int(formDetails.get("tournamentID"))
    winnerID = int(formDetails.get("winner"))
    matchID = int(formDetails.get("matchID"))
    roundNumber = int(formDetails.get("roundNumber"))
    playerName = formDetails.get("playerName")
    #return formDetails
    #updating winner on the database
    db.updateWinner(tournamentID, winnerID, matchID)
    #check if all games with roundnumber winner is from have a winner
    #do this by grabbing all games and checking if winner id is not none
    matchIDs = db.fetchMatches(tournamentID, roundNumber)
    isError = False
    for match in matchIDs:
        if db.fetchWinner(match[0]) == None:
            isError == True
        if isError == True:
        #if one id is none do nothing else and return to bracketview
            print("someone has yet to win")
            return redirect(url_for("pages.onView", tournamentID = tournamentID))
        #if yes checks if this is not the final round of the tournament
        #do this by fetching size and checking if round number is equal to log2size
        tournamentSize = db.fetchTournamentSize(tournamentID)
        print(int(math.log2(tournamentSize)))
        #if no declare winner and return player to bracketview
    if int(math.log2(tournamentSize)) == roundNumber:
        flash(str(playerName) + "has won the tournament!")
        return redirect(url_for("pages.onView", tournamentID = tournamentID))
    else:
        #if yes create all next round matches by fetching all winners from round
        winnersIDs = []
        for match in matchIDs:
            winnersIDs.append(db.fetchWinner(match[0]))
            #do this by pairing winners based on playerID where 2 smallest values pair up then the next and so on
            #this should somewhat already happen with how matchIDs are structured and how matches are made
        for i in range(0, int(len(winnersIDs)), 2):
            #create a match
            matchid = db.createMatches(tournamentID, (int(roundNumber) + 1))
            #then create match entries for each player based on these pairings and match that was just made
            db.createMatchEntry(matchid, winnersIDs[i])
            db.createMatchEntry(matchid, winnersIDs[i+1])
    #return user to bracket
    return redirect(url_for("pages.onView", tournamentID = tournamentID))