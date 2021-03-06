#generated automatically
from SqlAlchemy import convertToJson, dict_as_obj
from WebSocketsHelpers import checkArguments, removeClosedConnection
import Card
from random import random
from math import floor
from WebSocketsHelpers import filterOpenedConnectionPlayers
cardsSubscribers = set()
async def shuffleCards(session, playersConnected):
	print(playersConnected)
	print(len(playersConnected))

	cards=[]
	for i in range(2, 15):
		for j in range(0, 4):
			if i==2 and len(playersConnected)==6:
				break
			cards.append(Card.Card(type=j, number=i, playerId=0))
			if i==2 and j==2 and len(playersConnected)==3:
				break
			if i==2 and j==1 and len(playersConnected)==5:
				break
	playerIndex = 0
	while len(cards) > 0:
		print(len(cards))
		card = cards[floor(random() * len(cards))]
		card.playerId = playersConnected[playerIndex]['player'].playerId
		newCard = Card.addCard(session, card)
		playersConnected[playerIndex]['cards'].append(newCard)
		playerIndex = (playerIndex + 1) % len(playersConnected)
		cards.remove(card)
	cards = Card.getCards(session)
	response = convertToJson({'operation' : 'get', 'table' : 'Cards', 'data' : cards})
	for player in playersConnected:
		 await player['socket'].send(response)

async def changeCards(session, playersConnected, looser, winner, numberCards):
	winnerCards = Card.getCardsByPlayerIdSorted(session, winner["player"].playerId)
	looserCards = Card.getCardsByPlayerIdSorted(session, looser["player"].playerId)
	print("change ", numberCards, "between winner ", winner["player"].name, "and ", looser["player"].name)
	print(winnerCards)
	for card in winnerCards:
		print(card.number)
	for index in range(0, numberCards):
		card = winnerCards[index]
		winner["cards"].remove(card)
		card.playerId = looser["player"].playerId
		card = Card.updateCard(session, card)
		looser["cards"].append(card)
	for index in range(len(looserCards) - numberCards, len(looserCards)):
		card = looserCards[index]
		looser["cards"].remove(card)
		card.playerId = winner["player"].playerId
		card = Card.updateCard(session, card)
		winner["cards"].append(card)
	#update score
	winner["score"] = winner["score"] + numberCards
	looser["score"] = looser["score"] - numberCards

	cards = Card.getCards(session)
	response = convertToJson({'operation' : 'get', 'table' : 'Cards', 'data' : cards})
	for player in playersConnected:
		 await player['socket'].send(response)

async def removeCardsFromPlayer(session, playersConnected, player):
	print("remove cards for player ", player["player"].name)
	player["cards"] = []
	Card.deleteAllCardsForAPlayer(session, player["player"].playerId)

	cards = Card.getCards(session)
	response = convertToJson({'operation' : 'get', 'table' : 'Cards', 'data' : cards})
	for player in filterOpenedConnectionPlayers(playersConnected):
		 await player['socket'].send(response)

async def cardSelected(session, playersConnected, data):
	global cardsSubscribers
	for player in playersConnected:
		if player['player'].playerId == data["cards"][0]['playerId']:
			print("player gasit",len(player['cards']), range(0, 15))
			for card in data["cards"]:
				for i in range(0, len(player['cards'])):
					print(i)
					cardP = player['cards'][i]
					if cardP.cardId == card['cardId']:
						print("carte gasita")
						player['cards'].remove(cardP)
						break
			
	for card in data["cards"]:
		card = Card.deleteCard(session, card['cardId'])
		response = convertToJson({'operation' : 'delete', 'table' : 'Cards', 'data' : card})
		cardsSubscribers = set(filter(removeClosedConnection, cardsSubscribers))
		for subscriber in cardsSubscribers:
			 await subscriber.send(response)
async def requestReceived(websocket, session, request):
	global cardsSubscribers
	#Websockets endpoints
	if request['operation'] == 'get':
		#get endpoint
		cards = Card.getCards(session)
		response = convertToJson({'operation' : 'get', 'table' : 'Cards', 'data' : cards})
		await websocket.send(response)
	
	elif request['operation'] == 'subscribe':
		#subscription endpoint
		cards = Card.getCards(session)
		response = convertToJson({'operation' : 'get', 'table' : 'Cards', 'data' : cards})
		cardsSubscribers.add(websocket)
		await websocket.send(response)
	
	elif request['operation'] == 'add':
		#add endpoint
		if checkArguments(request, ['playerId', 'type', 'number']) == False:
			print('Not all parameters were provided for ADD in Cards')
			await websocket.send(convertToJson({'error' : 'Invalid request'}))
			return
		card = dict_as_obj(request['data'], Card.Card(), ['cardId', 'creationTime'])
		card = Card.addCard(session, card)
		response = convertToJson({'operation' : 'add', 'table' : 'Cards', 'data' : card})
		cardsSubscribers = set(filter(removeClosedConnection, cardsSubscribers))
		for subscriber in cardsSubscribers:
			 await subscriber.send(response)
	
	elif request['operation'] == 'update':
		#update endpoint
		if checkArguments(request, ['cardId']) == False:
			print('Not all parameters were provided for UPDATE in Cards')
			await websocket.send(convertToJson({'error' : 'Invalid request'}))
			return
		data = request['data']
		card = Card.getCardsByCardId(session, data['cardId'])[0]
		card = dict_as_obj(data, card)
		card = Card.updateCard(session, card)
		response = convertToJson({'operation' : 'update', 'table' : 'Cards', 'data' : card})
		cardsSubscribers = set(filter(removeClosedConnection, cardsSubscribers))
		for subscriber in cardsSubscribers:
			 await subscriber.send(response)
	
	elif request['operation'] == 'delete':
		#delete endpoint
		if checkArguments(request, ['cardId']) == False:
			print('Not all parameters were provided for DELETE in Cards')
			await websocket.send(convertToJson({'error' : 'Invalid request'}))
			return
		card = Card.deleteCard(session, request['data']['cardId'])
		response = convertToJson({'operation' : 'delete', 'table' : 'Cards', 'data' : card})
		cardsSubscribers = set(filter(removeClosedConnection, cardsSubscribers))
		for subscriber in cardsSubscribers:
			 await subscriber.send(response)
	
	

