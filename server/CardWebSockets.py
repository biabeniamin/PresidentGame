#generated automatically
from SqlAlchemy import convertToJson, dict_as_obj
from WebSocketsHelpers import checkArguments, removeClosedConnection
import Card
cardsSubscribers = set()
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
	
	

