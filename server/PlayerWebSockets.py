#generated automatically
from SqlAlchemy import convertToJson, dict_as_obj
from WebSocketsHelpers import checkArguments, removeClosedConnection
import Player
playersConnected = []
playersSubscribers = set()
async def requestReceived(websocket, session, request):
	global playersSubscribers
	#Websockets endpoints
	if request['operation'] == 'get':
		#get endpoint
		players = Player.getPlayers(session)
		response = convertToJson({'operation' : 'get', 'table' : 'Players', 'data' : players})
		await websocket.send(response)
	
	elif request['operation'] == 'subscribe':
		#subscription endpoint
		players = Player.getPlayers(session)
		response = convertToJson({'operation' : 'get', 'table' : 'Players', 'data' : players})
		playersSubscribers.add(websocket)
		await websocket.send(response)
	
	elif request['operation'] == 'add':
		#add endpoint
		if checkArguments(request, ['name', 'type']) == False:
			print('Not all parameters were provided for ADD in Players')
			await websocket.send(convertToJson({'error' : 'Invalid request'}))
			return
		player = dict_as_obj(request['data'], Player.Player(), ['playerId', 'creationTime'])
		player = Player.addPlayer(session, player)
		playersConnected.append({'player':player, 'socket':websocket})

		#inform player
		response = convertToJson({'operation' : 'registered', 'table' : 'Game', 'data' : player})
		await websocket.send(response)

		response = convertToJson({'operation' : 'add', 'table' : 'Players', 'data' : player})
		playersSubscribers = set(filter(removeClosedConnection, playersSubscribers))
		for subscriber in playersSubscribers:
			 await subscriber.send(response)
	
	elif request['operation'] == 'update':
		#update endpoint
		if checkArguments(request, ['playerId']) == False:
			print('Not all parameters were provided for UPDATE in Players')
			await websocket.send(convertToJson({'error' : 'Invalid request'}))
			return
		data = request['data']
		player = Player.getPlayersByPlayerId(session, data['playerId'])[0]
		player = dict_as_obj(data, player)
		player = Player.updatePlayer(session, player)
		response = convertToJson({'operation' : 'update', 'table' : 'Players', 'data' : player})
		playersSubscribers = set(filter(removeClosedConnection, playersSubscribers))
		for subscriber in playersSubscribers:
			 await subscriber.send(response)
	
	elif request['operation'] == 'delete':
		#delete endpoint
		if checkArguments(request, ['playerId']) == False:
			print('Not all parameters were provided for DELETE in Players')
			await websocket.send(convertToJson({'error' : 'Invalid request'}))
			return
		player = Player.deletePlayer(session, request['data']['playerId'])
		response = convertToJson({'operation' : 'delete', 'table' : 'Players', 'data' : player})
		playersSubscribers = set(filter(removeClosedConnection, playersSubscribers))
		for subscriber in playersSubscribers:
			 await subscriber.send(response)
	
	

