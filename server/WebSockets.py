#generated automatically
import asyncio
import websockets
import json
from SqlAlchemyMain import session
import CardWebSockets
from SqlAlchemy import convertToJson, dict_as_obj
import PlayerWebSockets
from PlayerWebSockets import playersConnected
import NotificationWebSockets
import Player
import Card

turn = 0

users = set()
def connectedSuccessfullyEvent():
	return json.dumps({'table': 'WebSockets', 'operation' : 'connectedSuccessfully'})

async def updateTurn():
	global turn
	if turn >= len(playersConnected):
		turn = 0
	await PlayerWebSockets.setTurn(session, turn)

async def controlRequestReceived(websocket, session, request):
	global playersSubscribers
	global turn
	#Websockets endpoints
	print("adsdas")
	if request['operation'] == 'start':
		#Card.deleteAllCards(session)
		#Player.deleteAllPlayers(session)
		await CardWebSockets.shuffleCards(session, playersConnected)
		turn = 0
		await updateTurn()
	elif request['operation'] == 'cardSelected':
		await CardWebSockets.cardSelected(session, playersConnected, request['data'])
		turn = turn + 1
		await updateTurn()
async def requestReceived(websocket, path):
	users.add(websocket)
	websocket.authenticated = False
	try:
		await websocket.send(connectedSuccessfullyEvent())
		print('client connected')
		async for requestJson in websocket:
			request = json.loads(requestJson)
			print(request)
			if request['table'] == 'Cards':
				await CardWebSockets.requestReceived(websocket, session, request)
			elif request['table'] == 'Players':
				await PlayerWebSockets.requestReceived(websocket, session, request)
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
