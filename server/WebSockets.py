#generated automatically
import asyncio
import websockets
import json
from SqlAlchemyMain import session
import CardWebSockets
from SqlAlchemy import convertToJson, dict_as_obj
import PlayerWebSockets
import NotificationWebSockets
import Player
import Card

turn = 0
lastCard = 0

playersConnected = []
users = set()
def connectedSuccessfullyEvent():
	return json.dumps({'table': 'WebSockets', 'operation' : 'connectedSuccessfully'})

async def updateTurn():
	global turn, playersConnected
	if turn >= len(playersConnected):
		turn = 0
	await PlayerWebSockets.setTurn(session, playersConnected, turn)

async def controlRequestReceived(websocket, session, request):
	global playersSubscribers
	global turn, playersConnected
	#Websockets endpoints
	print("adsdas")
	if request['operation'] == 'start':
		#Card.deleteAllCards(session)
		#Player.deleteAllPlayers(session)
		await CardWebSockets.shuffleCards(session, playersConnected)
		print(playersConnected)
		turn = 0
		await updateTurn()
	elif request['operation'] == 'cardSelected':
		await CardWebSockets.cardSelected(session, playersConnected, request['data'])
		
		for player in playersConnected:
			response = convertToJson({'operation' : 'get', 'table' : 'Cards2', 'data' : player['cards']})
			await player['socket'].send(response)
		lastCard = request['data']
		foundBigger = False
		for player in playersConnected:
			if foundBigger:
				break
			for card in player['cards']:
				if card.number > request['data']['number']:
					foundBigger = True
					print("gasita mai mare la ", card.playerId)
					break
				
		
		if foundBigger == True:
			turn = turn + 1
			await updateTurn()
async def requestReceived(websocket, path):
	users.add(websocket)
	websocket.authenticated = False
	try:
		print('client connected')
		await websocket.send(connectedSuccessfullyEvent())
		print('client connected')
		async for requestJson in websocket:
			request = json.loads(requestJson)
			print(request)
			if request['table'] == 'Cards':
				await CardWebSockets.requestReceived(websocket, session, request)
			elif request['table'] == 'Players':
				await PlayerWebSockets.requestReceived(websocket, session, playersConnected, request)
			elif request['table'] == 'Notifications':
				await NotificationWebSockets.requestReceived(websocket, session, request)
			elif request['table'] == 'Control':
				await controlRequestReceived(websocket, session, request)
	
	finally:
		print('client disconnected')
		users.remove(websocket)
	

Card.deleteAllCards(session)
Player.deleteAllPlayers(session)
start_server = websockets.serve(requestReceived, 'localhost', 6789)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
