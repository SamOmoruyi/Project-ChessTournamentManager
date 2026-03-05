from sqlite3 import connect
import sqlite3 as sql

def roundmaker():
    bracket = []
    round = []
    n = int(input("Type no. of rounds"))
    while n != 0:
        if n == 1:
            final = []
            bracket.append(final)
        if n == 2:
            semiFinal = []
            bracket.append(semiFinal)
        if n == 3:
            quarterFinal = []
            bracket.append(quarterFinal)
        if n == 4:
            roundOf16 = []
            bracket.append(roundOf16)
        n = n - 1
    y = "find me!"
    final.append("find me!")
    final.append("other")
    print(bracket)
    print(len(bracket))
    if y in final:
         print("found successfully :)")
         print(final.index(y))

def connect():
        return sql.connect(dbName)

def fetchAllMatchIDs():
        with connect() as conn:
            conn.cursor()
            results = conn.execute("SELECT matchID FROM matches")
            matchIDs = results.fetchall()
            return matchIDs

def createMatchesTable():
        with connect() as conn:
            conn.cursor()
            conn.execute("""CREATE TABLE IF NOT EXISTS matches (
                         matchID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                         topID INTEGER,
                         botID INTEGER,
                         matchOutcome INTEGER )""")
            conn.commit()
        
def createMatch():
      with connect() as conn:
            conn.cursor()
            conn.execute("""INSERT into matches""")
            conn.commit()

def sizeMaker():
    n = int(input("*waiting for u to select size...*"))
    possibleSizes = [2, 4, 8, 16]
    if n not in possibleSizes:
          print("INVALID SIZE!")
    print(n)

dbName = "testDatabase.db"

roundmaker()