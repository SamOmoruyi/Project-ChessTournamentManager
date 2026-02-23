from database import DataBaseHandler
import flask
import math

tournaments = Blueprint("tournaments",__name__,url_prefix="/tournaments")

@tournaments.route("/createtournament", methods = ["POST"])
def createTournament():
    formDeatils = request.form
    tournamentName = formDeatils.get("tournamentName")
    tournamentDescription = formDeatils.get("tournamentDescription")
    tournamentDate = formDeatils.get("tournamentDate")
    tournamentSize = formDeatils.get("tournamentSize")
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
        return redirect(url_for(pages.createTournament))
    db = DataBaseHandler()
    username = session["currentUser"]
    userID = db.fetchUserID(username)
    success, errorType = db.addTournament(userID, tournamentName, tournamentDate, tournamentDescription, tournamentSize)
    if success:
        return redirect(url_for("pages.tournamentplayerselection"))
    if errorType == "integrity-error":
        flash("Invalid data has been entered - Please try again")
    elif errorType == "unique-error":
        flash("Tournament name taken - Please use a different username")
    else:
        flash("An error has occurred")
    return redirect(url_for("pages.createtournament", tournamentName = tournamentName))

@tournaments.route("/createplayers", methods = ["POST"])
def createPlayers():
    db = DataBaseHandler()
    tournamentName = session[tournamentName] 
    tournamentID = db.fetchTournamentID(tournamentName)
    tournamentSize = db.fetchTournamentSize(tournamentID)
    for i in range(tournamentSize - 1):
        formDetails = request.form
        playerName = formDetails.get("playerName")
        db.addPlayer(playerName, tournamentID)
    #bit that makes the matches
    for i in range(tournamentSize - 2):
        db.createMatches(tournamentID)    
    return redirect(url_for("pages.bracketview", tournamentID = tournamentID, tournamentSize = tournamentSize, ))

