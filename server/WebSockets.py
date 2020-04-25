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

users = set()
def connectedSuccessfullyEvent():
	return json.dumps({'table': 'WebSockets', 'operation' : 'connectedSuccessfully'})


async def controlRequestReceived(websocket, session, request):
	global playersSubscribers
	#Websockets endpoints
	print("adsdas")
	if request['operation'] == 'start':
		#Card.deleteAllCards(session)
		#Player.deleteAllPlayers(session)
		await CardWebSockets.shuffleCards(session, playersConnected)
		#response = convertToJson({'operation' : 'get', 'table' : 'Players', 'data' : playersConnected})
		#await websocket.send(response)
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
