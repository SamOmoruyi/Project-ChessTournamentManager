from flask import Blueprint, flash, redirect, request, session, url_for
from database import DataBaseHandler
# setup of blueprint
auth = Blueprint("auth",__name__,url_prefix="/auth")
# authorise user function in order to validate user login details from the server-side
@auth.route("/authoriseuser", methods = ["POST"])
def authoriseUser():
    formDetails = request.form
    username = formDetails.get("username")
    email = formDetails.get("email")
    password = formDetails.get("password")
    db = DataBaseHandler()
    success = db.authoriseUser(username, email, password)
    if success:
        session["currentUser"] = username
        return redirect(url_for("pages.dashboard"))    
    return redirect(url_for("pages.login"))
 
@auth.route("/createuser", methods = ["POST"])
# function which creates a user properly through website details instead of hard-coding details manually
def createUser():
    formDetails = request.form
    username = formDetails.get("username")
    email = formDetails.get("email")
    password = formDetails.get("password")
    repassword = formDetails.get("repassword")
    errors = False
    #error checking and outputting suitable error messages
    if password != repassword:
        flash("Passwords do not match - Please try again.")
        errors = True
    if len(password) < 8:
        flash("Password must be 8 or more characters - Please try again.")    
        errors = True
    if len(username) < 4:
        flash("Username must be longer than 3 characters - Please try again.")
        errors = True
    if errors:
        return redirect(url_for("pages.signup"))
    db = DataBaseHandler()
    success, errorType = db.createUser(username, email, password)
    if success:
        return redirect(url_for("pages.dashboard")) 
    if errorType == "integrity-error":
        flash("Invalid data has been entered - Please try again")
    elif errorType == "unique-error":
        flash("Username taken - Please use a different username")
    else:
        flash("An error has occurred")
    return redirect(url_for("pages.signup"))
# simple signout function
@auth.route("/signout")
def signOut():
    session.clear()
    return redirect(url_for("pages.guestdashboard"))
