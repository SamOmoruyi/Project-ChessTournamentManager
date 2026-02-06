from flask import session
#only purpose is to return currently logged in user 
def isAuthorised():
    return "currentUser" in session
