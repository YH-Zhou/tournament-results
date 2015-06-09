#!/usr/bin/env python
# tournament.py -- implementation of a Swiss-system tournament

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    # Open a cursor to perform database operations
    cursor = conn.cursor()
    query = "DELETE FROM Matches;"
    # Execute a sql command
    cursor.execute(query)
    # Make the changes to the database persistent
    conn.commit()
    # Close communication with the database
    conn.close()
    cursor.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    # Open a cursor to perform database operations
    cursor = conn.cursor()
    query = "DELETE FROM Players;"
    # Execute a sql command
    cursor.execute(query)
    # Make the changes to the database persistent
    conn.commit()
    conn.close()
    cursor.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    # Open a cursor to perform database operations
    cursor = conn.cursor()
    query = "SELECT COUNT(PlayerID) FROM Players;"
    cursor.execute(query)
    # Retrieves the next row of the query result set
    playersNumber = cursor.fetchone()[0]
    conn.close()
    cursor.close()
    return playersNumber


def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    # Open a cursor to perform database operations
    cursor = conn.cursor()
    query = "INSERT INTO Players (PlayerName) VALUES (%s);"
    # Execute a sql command
    cursor.execute(query, (name, ))
    conn.commit()
    conn.close()
    cursor.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    # Open a cursor to perform database operations
    cursor = conn.cursor()
    query = "SELECT * FROM player_standings;"
    # Execute a sql command
    cursor.execute(query)
    standings = cursor.fetchall()
    conn.close()
    cursor.close()
    return standings


def playerStandingsOMW():
    """ Returns a list of the players and their win records, sorted
        by their wins and opponent match wins (When two players have
        the same number of wins, rank them according to the total
        number of wins by players they have played against).
    Returns:
        A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id(assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    # Open a cursor to perform database operations
    cursor = conn.cursor()
    query = "SELECT * FROM player_standings_omw;"
    # Execute a sql command
    cursor.execute(query)
    # Retrieves all the rows of the query result set
    standings = cursor.fetchall()
    # Close communication with the database
    conn.close()
    cursor.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    # Open a cursor to perform database operations
    cursor = conn.cursor()
    query = "INSERT INTO Matches (Player1_ID, Player2_ID, Winner, Loser) \
             VALUES (%s, %s, %s, %s);"
    # Execute a sql command with the given arguments
    cursor.execute(query, (winner, loser, winner, loser, ))
    # Make the changes to the database persistent
    conn.commit()
    conn.close()
    cursor.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    pairings = []
    paired = []
    for player in standings:
        if len(paired) < 4:
            paired.append(player[0])
            paired.append(player[1])
        if len(paired) == 4:
            pairings.append(tuple(paired))
            paired = []
    return pairings
