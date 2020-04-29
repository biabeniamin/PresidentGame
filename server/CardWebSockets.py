#generated automatically
from SqlAlchemy import convertToJson, dict_as_obj
from WebSocketsHelpers import checkArguments, removeClosedConnection
import Card
from random import random
from math import floor
cardsSubscribers = set()
async def shuffleCards(session, playersConnected):
	print(playersConnected)
	print(len(playersConnected))

	cards=[]
	for i in range(12, 15):
		for j in range(0, 4):
			cards.append(Card.Card(type=j, number=i, playerId=0))
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
async def cardSelected(session, playersConnected, card):
	global cardsSubscribers
	for player in playersConnected:
		if player['player'].playerId == card['playerId']:
			print("player gasit",len(player['cards']), range(0, 15))
			for i in range(0, len(player['cards'])):
				print(i)
				cardP = player['cards'][i]
				if cardP.cardId == card['cardId']:
					print("carte gasita")
					player['cards'].remove(cardP)
					break
			
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
	
	

