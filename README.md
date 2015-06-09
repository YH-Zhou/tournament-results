# Tournament Planner

Develop a database schema to store details of a games matches between players. And write a Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament.This game tournament uses the Swiss system for pairing up players in each round: players are not eliminated, and each player should be paired with another player with the same number of wins, or as close as possible.


## Table of contents

- [Requirements](#requirements)
- [Files](#files)
- [Instructions](#instructions)
- [Expected Outcomes](#expectedoutcomes)
- [Support](#support)


## Requirements

- Download [python](https://www.python.org/downloads/) on your computer;
- Download the following files: tournament.py, tournament_test.py and tournament.sql;
- Install the [vagrant virtual machine](https://www.vagrantup.com/downloads) on your computer.


## Files

* tournament.py : The python implementation of the swiss tournament.
* tournament.sql : SQL code that creates a tournament database with well designed tables 	and views. 
* tournament_test.py : Contains some test cases for tournament.py.


## Instructions

- To run the Vagrant Virtual Machine, in the terminal use the command 'vagrant up' followed by 'vagrant ssh'. Once you have executed the vagrant ssh command, you can execute the command 'cd /vagrant' to change the directory to the folders where you store the downloaded module files;
- To build and access the tournament database, type 'psql' in the command line followed by 
	'\i tournament.sql';
- To quit psql, type '\q' int the command line;
- Then in the terminal, type 'python tournament_test.py' to run the tests for the module tournament.py.


## Expected Outcomes

vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ python tournament_test.py 
1. Old matches can be deleted.
2. Player records can be deleted.
3. After deleting, countPlayers() returns zero.
4. After registering a player, countPlayers() returns 1.
5. Players can be registered and deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After one match, players with one win are paired.
9. OMW is implemented correctly
10. Success!  All tests pass!


## Support

If you have any issues about the movie trailer website, please let me know.
My email address is yanhong.zhou05@gmail.com.