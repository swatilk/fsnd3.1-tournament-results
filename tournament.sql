-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table players (player_id SERIAL primary key, full_name varchar(20));
create table matches (match_id SERIAL primary key, winner int, loser int, foreign key (winner) references players (player_id), foreign key (loser) references players (player_id));
create view standings as select player_id, full_name, (select count(matches.winner) from matches where player_id = matches.winner) as wins,(select count(matches.match_id) from matches where player_id = matches.winner OR player_id = matches.loser) as matches from Players Order by wins desc, matches desc;


