-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes,
-- like these lines here.


-- Create database "tournament" and connect
-- to that database before creating tables
\c vagrant
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament


-- Create table "Players" to store the player ID and player name.
CREATE TABLE Players (
	PlayerID SERIAL PRIMARY KEY,
	PlayerName VARCHAR(255)
);

-- Create table "Matches" to store the player IDs and winner/loser.
CREATE TABLE Matches (
	MatchID SERIAL PRIMARY KEY,
	Player1_ID SERIAL REFERENCES Players (PlayerID),
	Player2_ID SERIAL REFERENCES Players (PlayerID),
	Winner SERIAL REFERENCES Players (PlayerID),
	Loser SERIAL REFERENCES Players (PlayerID)
);

-- Create view "number_of_matches" to store the player ID, player name
-- and the total number of matches each player played.
CREATE VIEW number_of_matches AS
	SELECT p.PlayerID, p.PlayerName, 
		   COALESCE(count(m.Player1_ID), 0) AS numOfMatches
	FROM Players AS p LEFT JOIN Matches AS m
		ON p.PlayerID = m.Player1_ID OR p.PlayerID = m.Player2_ID
	GROUP BY p.PlayerID;

-- Create view "number_of_wins" to store the player ID, player name
-- and the total number of matches that each player had won.
CREATE VIEW number_of_wins AS 
	SELECT p.PlayerID, p.PlayerName, 
		   COALESCE(count(m.Winner), 0) AS numOfWins
	FROM Players AS p LEFT JOIN Matches AS m
		ON p.PlayerID = m.Winner
	GROUP BY p.PlayerID;

-- Create view "player_standings" to show the rank of the players
-- according to their number of wins.
CREATE VIEW player_standings AS
	SELECT nm.PlayerID, nm.PlayerName, 
		   nw.numOfWins, nm.numOfMatches
	FROM number_of_matches AS nm  
		LEFT JOIN number_of_wins AS nw
			ON nw.PlayerID = nm.PlayerID
	ORDER BY nw.numOfWins DESC;

-- Create view "player_omw" to show the total number of wins that
-- all opponents of each player had won.
CREATE VIEW player_omw AS
	SELECT oppo.Winner, COALESCE(sum(nw.numOfWins), 0) AS omw
	FROM number_of_wins AS nw LEFT JOIN 
		(
			SELECT w.Winner, w.Loser FROM Matches as w
			UNION ALL
			SELECT l.Loser, l.Winner FROM Matches as l
		) AS oppo
			ON nw.PlayerID = oppo.Loser
	GROUP BY oppo.Winner;

-- Create view "player_standings_omw" to show the rank of each
-- player according to their own number of wins and their opponent
-- match wins.
CREATE VIEW player_standings_omw AS
	SELECT ps.PlayerID, ps.PlayerName, ps.numOfWins, ps.numOfMatches
	FROM player_standings AS ps
		LEFT JOIN player_omw AS OMW
			ON ps.PlayerID = OMW.Winner
	ORDER BY ps.numOfWins DESC, OMW.omw DESC;
