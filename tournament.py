#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2, bleach

DBNAME = "tournament"

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect(database=DBNAME)


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    result = c.execute("truncate matches cascade")
    db.commit()
    db.close()
    return result


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    result = c.execute("truncate players cascade")
    db.commit()
    db.close()
    return result

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    #http://www.postgresqltutorial.com/postgresql-count-function/
    c.execute("select count(player_id) from Players")
    results = c.fetchone()[0]
    db.close()
    return results


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    text = bleach.clean(str(name))
    c.execute("insert into Players (full_name) values (%s)" ,(text,))
    db.commit()
    db.close()



def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    c.execute("select * from standings")
    db.commit()
    result = c.fetchall()
    db.close()
    return result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into matches (winner, loser) values (%s, %s)", (winner, loser))
    c.execute("select * from matches")
    db.commit()
    result = c.fetchall()
    db.close()


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
    db = connect()
    c = db.cursor()
    c.execute("select * from standings order by wins desc")
    db.commit()
    standings = c.fetchall()
    i = 0
    results = []
    while i < len(standings):
        tupple = (standings[i][0], standings[i][1], standings[i+1][0], standings[i+1][1]);
        results.append(tupple)
        i += 2
    db.close()
    return results


