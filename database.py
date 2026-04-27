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
            #conn.execute("DROP TABLE users")
            #conn.execute("DROP TABLE tournaments")
            #conn.execute("DROP TABLE players")
            #conn.execute("DROP TABLE matches")
            #conn.execute("DROP TABLE matchEntry")
            self.createUsersTable()
            self.createTournamentsTable()
            self.createPlayersTable()
            self.createMatchesTables()
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
    #making procedure to delete users from the Users Table
    def deleteUser(self, userID):
        with self.connect() as conn:
            conn.execute("DELETE FROM users WHERE userID = ?", (userID))
            conn.commit()
            
    #making function that authorises users 
    def authoriseUser(self, username, password):
        try:
            with self.connect() as conn:
                # collecting results from creating a user into one variable
                results = conn.execute("SELECT userID FROM users WHERE username = ? AND password = ?", (username, password))
                # fetching results so that other functions can make use of them
                userID = results.fetchone()
                conn.commit()
                if userID != None:
                    return True, userID[0]
                else:
                    return False, None

        except:
            return False, None

    def createTournamentsTable(self):

        with self.connect() as conn:
            conn.cursor()
            conn.execute("""CREATE TABLE IF NOT EXISTS tournaments (
                         tournamentID INTEGER PRIMARY KEY AUTOINCREMENT,
                         userID INTEGER NOT NULL,
                         tournamentName TEXT UNIQUE NOT NULL,
                         tournamentDescription TEXT NOT NULL,
                         tournamentDate DATE NOT NULL,
                         tournamentSize INTEGER NOT NULL,
                         FOREIGN KEY (userID) REFERENCES users(userID) ON DELETE CASCADE
                         );""")
            conn.commit()

    def createUsersTable(self):
        with self.connect() as conn:
            conn.cursor()
            conn.execute("""CREATE TABLE IF NOT EXISTS users (
                         userID INTEGER PRIMARY KEY AUTOINCREMENT,
                         userName TEXT UNIQUE NOT NULL CHECK(length(userName) > 3),
                         email TEXT NOT NULL,
                         password TEXT NOT NULL CHECK(length(password) > 7)
                         );""")
            conn.commit()
    def deleteTournament(self, tournamentID, userID):
        with self.connect() as conn:
                conn.cursor()
                conn.execute("""DELETE FROM tournaments WHERE tournamentID = ? AND userID = ?""", (tournamentID, userID))
                conn.commit()

    def fetchTournaments(self):
        with self.connect() as conn:
            conn.cursor()
            results = conn.execute("SELECT tournamentID, tournamentName, tournamentDescription, tournamentSize, tournamentDate FROM tournaments")
            conn.commit()
            tournaments = results.fetchall()
            return tournaments
        
    def fetchTournament(self, tournamentID):
        with self.connect() as conn:
            conn.cursor()
            results = conn.execute("SELECT tournamentName, tournamentDescription, tournamentSize, tournamentDate, userID FROM tournaments WHERE tournamentID = ?", (tournamentID,))
            conn.commit()
            tournament = results.fetchall()
            return tournament
        
    def fetchTournamentsByUser(self, userID):
        with self.connect() as conn:
            conn.cursor()
            results = conn.execute("SELECT tournamentID, tournamentName, tournamentDescription, tournamentSize, tournamentDate FROM tournaments WHERE userID = ?", (userID,))
            conn.commit()
            tournaments = results.fetchall()
            return tournaments

    def addTournament(self, userID, tournamentName, tournamentDate, tournamentDescription, tournamentSize):
        try:
            with self.connect() as conn:
                conn.cursor()
                conn.execute("INSERT INTO tournaments (userID, tournamentName, tournamentDate, tournamentDescription, tournamentSize) VALUES (?, ?, ?, ?, ?);", (userID, tournamentName, tournamentDate, tournamentDescription, tournamentSize))
                results = conn.execute(" SELECT last_insert_rowid();")
                returnedID = results.fetchone()
                # print(returnedID)
                conn.commit()
                return True, returnedID[0]
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
        
    def createPlayersTable(self):
        with self.connect() as conn:
            conn.cursor()
            conn.execute("""CREATE TABLE IF NOT EXISTS players (
                         playerID INTEGER PRIMARY KEY AUTOINCREMENT,
                         tournamentID INTEGER NOT NULL,
                         playerName TEXT NOT NULL,
                         FOREIGN KEY (tournamentID) REFERENCES tournaments(tournamentID) ON DELETE CASCADE
                         )""")
            conn.commit()

    def getAllTournamentMatches(self, tournamentID):
        matchDetails = []
        with self.connect() as conn:
            matches = conn.execute("""
            SELECT matchID 
            FROM matches 
            WHERE tournamentID = ?;
            """, (tournamentID, )).fetchall()
            print(matches)
            for match in matches:
                matchDetails.append(conn.execute("""
                    SELECT players.playerName, players.playerID, matchEntry.matchID
                    FROM players 
                    JOIN matchEntry
                    ON matchEntry.playerID = players.playerID 
                    WHERE matchEntry.matchID = ?""", (match,)).fetchall())
        print("matchdetails", matchDetails)
        return matchDetails
        
            

    def addPlayer(self, playerName, tournamentID):
            with self.connect() as conn:
                conn.execute("INSERT INTO players (playerName, tournamentID) VALUES (?, ?)",(playerName, tournamentID))
                results = conn.execute("SELECT last_insert_rowid();")
                playerID = results.fetchone()
                conn.commit()
                return playerID[0]

    def createMatchesTables(self):
        with self.connect() as conn:
            conn.cursor()
       
            conn.execute("""CREATE TABLE IF NOT EXISTS matchEntry (
                            matchEntryID INTEGER PRIMARY KEY AUTOINCREMENT,
                            matchID INTEGER,
                            playerID INTEGER,
                            FOREIGN KEY (matchID) REFERENCES matches(matchID) ON DELETE CASCADE,
                            FOREIGN KEY (playerID) REFERENCES players(playerID)                         
                         )""")

            conn.execute("""CREATE TABLE IF NOT EXISTS matches (
                         matchID INTEGER PRIMARY KEY AUTOINCREMENT,
                         tournamentID INTEGER NOT NULL,
                         round INTERGER,
                         winnerID INTEGER DEFAULT NULL,
                         FOREIGN KEY (tournamentID) REFERENCES tournaments(tournamentID) ON DELETE CASCADE)""")
            conn.commit()

    def createMatches(self, tournamentID, round):
        with self.connect() as conn:
            conn.cursor()
            conn.execute("INSERT INTO matches (tournamentID, round) VALUES (?, ?)",(tournamentID,round,))
            results = conn.execute("SELECT last_insert_rowid();")
            matchID = results.fetchone() 
            conn.commit()
            return matchID[0]

    def createMatchEntry(self, matchID, playerID):
        with self.connect() as conn:
            conn.cursor()
            conn.execute("INSERT INTO matchEntry (matchID, playerID) VALUES (?, ?)", (matchID, playerID))
            conn.commit()

    def updateWinner(self, tournamentID, newWinner, matchID):
        with self.connect() as conn:
            conn.cursor()
            conn.execute("UPDATE matches SET winnerID = ? WHERE tournamentID= ? AND matchID  = ?", (newWinner, tournamentID, matchID))
            conn.commit()
            return newWinner

    def getAllMatchDetails(self, tournamentID):
        with self.connect() as conn:
            conn.cursor()
            results = conn.execute("""SELECT players.playerName, players.playerID, matches.matchID, matches.winnerID, matches.round
                            FROM players
                            JOIN matchEntry ON players.playerID = matchEntry.playerID
                            JOIN matches ON matchEntry.matchID = matches.matchID
                            WHERE matches.tournamentID = ?""", (tournamentID, ))
            matchDetails = results.fetchall()
            return matchDetails
        
    def fetchTournamentID(self, tournamentName):
        with self.connect() as conn:
            conn.cursor()
            results = conn.execute("SELECT tournamentID FROM tournaments WHERE tournamentName = ?", (tournamentName,))
            tournamentID = results.fetchone()
            return tournamentID
    
    def fetchTournamentSize(self,tournamentID):
        with self.connect() as conn:
            conn.cursor()
            results = conn.execute("SELECT tournamentSize FROM tournaments WHERE tournamentID = ?", (tournamentID,))
            tournamentSize = results.fetchone()
            return tournamentSize[0]

    def fetchAllMatchIDs(self, tournamentID):
        with self.connect() as conn:
            conn.cursor()
            results = conn.execute("SELECT matchID FROM matches WHERE tournamentID = ?", (tournamentID,))
            matchIDs = results.fetchall()
            return matchIDs
        
    def fetchMatchEntries(self, matchID):
        with self.connect() as conn:
            conn.cursor()
            results = conn.execute("SELECT playerID FROM matchEntry WHERE matchID = ?", (matchID,))
            matchEntries = results.fetchall()
            return matchEntries
        
    def fetchPlayerID(self, playerName, tournamentID):
        try:
            with self.connect() as conn:
                conn.cursor()
                results = conn.execute("SELECT playerID FROM players WHERE playerName = ? AND tournamentID = ?", (playerName, tournamentID,))
                playerID = results.fetchone()
                if playerID != None:
                    return playerID[0], True
                else:
                    return None, False
        except:
            return None, False
        
    def fetchAllPlayerIDs(self, tournamentID):
        with self.connect() as conn:
            conn.cursor()
            results = conn.execute("SELECT playerID FROM players WHERE tournamentID = ?", (tournamentID,))
            playerIDs = results.fetchall()
            return playerIDs
        
    def fetchPlayerName(self, playerID):
        with self.connect() as conn:
            conn.cursor()
            results = conn.execute("SELECT playerName from players WHERE playerID = ?",(playerID,))
            playerNames = results.fetchone()
            return playerNames
        
    def fetchMatches(self, tournamentID, round):
        with self.connect() as conn:
            conn.cursor()
            results = conn.execute("SELECT matchID FROM matches WHERE tournamentID = ? AND round = ?", (tournamentID, round, ))
            matchIDs = results.fetchall()
            return matchIDs

    def fetchWinner(self, matchID):
        with self.connect() as conn:
            conn.cursor()
            results = conn.execute("SELECT winnerID FROM matches WHERE matchID = ?", (matchID, ))
            winner = results.fetchone()
            return winner[0]

db = DataBaseHandler()
db.createTable()