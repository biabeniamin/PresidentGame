
#generated automatically
from SqlAlchemyMain import createDatabase, session
from CardEndpoints import CardEndpoints
from PlayerEndpoints import PlayerEndpoints
from NotificationEndpoints import NotificationEndpoints

import Card
import Player

def init():
	#delete
	cards=Card.getCards(session)
	for card in cards:
		Card.deleteCard(session, card.cardId)
	players=Player.getPlayers(session)
	for player in players:
		Player.deletePlayer(session, player.playerId)
	#add
	deck=Player.addPlayer(session, Player.Player(name="Deck", type=0))
	mat=Player.addPlayer(session, Player.Player(name="Mat", type=1))
	player1=Player.addPlayer(session, Player.Player(name="Player1", type=2))
	player2=Player.addPlayer(session, Player.Player(name="Player2", type=2))
	player3=Player.addPlayer(session, Player.Player(name="Player3", type=2))
	player4=Player.addPlayer(session, Player.Player(name="Player4", type=2))

	for i in range(2, 15):
		for j in range(0, 4):
			Card.addCard(session, Card.Card(type=j, number=i, playerId=deck.playerId))

init()
