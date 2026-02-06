#importing sql in order to use it within this file while short handing it so that it is easier to type
import sqlite3 as sql
class DataBaseHandler:
    # setting up class as well as making the database file  
    def __init__(self, dbName = "appData.db"):
        self.dbName = dbName
    # creating the function that connects the python file and the database file
    def connect(self):
        return sql.connect(self.dbName)
    def createTable(self):
        #shortening sql.connect so it can be easier to type (not important now but needs to stay consistent for later)
        with self.connect() as conn:  
            conn.cursor()
            #users creation 
            conn.execute("""CREATE TABLE IF NOT EXISTS users (
                         userID INTEGER PRIMARY KEY AUTOINCREMENT,
                         userName TEXT UNIQUE NOT NULL CHECK(length(userName) > 3),
                         email TEXT NOT NULL,
                         password TEXT NOT NULL CHECK(length(password) > 7)
                         );""")
            #tournaments creation
            conn.execute("""CREATE TABLE IF NOT EXISTS tournaments (
                         tournamentID INTEGER PRIMARY KEY AUTOINCREMENT,
                         userID INTERGER NOT NULL,
                         tournamentName TEXT NOT NULL,
                         tournamentStatus TEXT NOT NULL DEFAULT incomplete CHECK(tournamentStatus IN ("incomplete,complete")),
                         tournamentDate TEXT NOT NULL,
                         tournamentLocation TEXT NOT NULL,
                         FOREIGN KEY (userID) REFERENCES users(userID) ON DELETE CASCADE
                         );""")
            #commit changes and close connection
            conn.commit()
    #making function which places user into table
    def createUser(self, userName, email, password):
        try:
            #main user insertion part of the algorithm
            with self.connect() as conn:
                conn.execute("INSERT INTO users (userName, email, password) VALUES (?, ?, ?)", (userName, email, password))
                conn.commit()
                return True, None
        #part of the algorithm used to track errors for the website in the future (with prints so I know what the errors are while the website does not exist)
        except sql.IntegrityError as error:
            print(error)
            if "UNIQUE" in str(error):
                print("unique-error")
                return False, "unique-error"
            else:
                print("integrity-error")
                return False, "integrity-error"
        except Exception as error:
            print(error)
            print("unkown-error")
            return False, "unknown-error"
    #making procedure to delete users from the Users Table will be hard coded for now and improved at a later stage
    def deleteUser(self):
        with self.connect() as conn:
            conn.execute("DELETE FROM users WHERE userID = 2")
            conn.commit()
            
    #making function that authorises users 
    def authoriseUser(self, username, email, password):
        try:
            with self.connect() as conn:
                # collecting results from creating a user into one variable
                results = conn.execute("SELECT userID FROM users WHERE username = ? AND email = ? AND password = ?", (username, email, password))
                # fetching results so that other functions can make use of them
                userDetails, userID = results.fetchone()
                conn.commit()
                return True, userID

        except:
            return False, None
        
db = DataBaseHandler()
db.createTable()
#db.deleteUser()