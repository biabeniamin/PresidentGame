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
from itertools import chain

turn = 0
lastCard = 0
indexPlayerLastCard = 0

playersConnected = []
users = set()
def connectedSuccessfullyEvent():
	return json.dumps({'table': 'WebSockets', 'operation' : 'connectedSuccessfully'})

async def jumpToNextPlayer():
	global playersConnected, turn, lastCard, indexPlayerLastCard
	foundBigger = False
	for i in chain(range(turn + 1, len(playersConnected)), range(0, turn)):
		player = playersConnected[i]
		if player['turnPassed'] == True:
			continue
		if foundBigger:
			break
		for card in player['cards']:
			if card.number > lastCard:
				foundBigger = True
				print("gasita mai mare la ", card.playerId)
				print("turn", turn, " ", i)
				if indexPlayerLastCard == i:
					lastCard = 0
				turn = i
				await updateTurn()
				break
	if foundBigger == False:
		lastCard = 0
		#reset passed turn
		for player in playersConnected:
			player['turnPassed'] = False
		await updateTurn()

async def updateTurn():
	global turn, playersConnected, lastCard
	if turn >= len(playersConnected):
		turn = 0
	print("set turn to ", turn, " and last card to ", lastCard)
	await PlayerWebSockets.setTurn(session, playersConnected, turn, lastCard)

async def controlRequestReceived(websocket, session, request):
	global playersSubscribers
	global turn, playersConnected, lastCard, indexPlayerLastCard
	#Websockets endpoints
	print("adsdas")
	if request['operation'] == 'start':
		#Card.deleteAllCards(session)
		#Player.deleteAllPlayers(session)
		await CardWebSockets.shuffleCards(session, playersConnected)
		print(playersConnected)
		turn = 0
		lastCard = 0
		await updateTurn()
	elif request['operation'] == 'cardSelected':
		await CardWebSockets.cardSelected(session, playersConnected, request['data'])
	
		for i in range(0, len(playersConnected)):
			if playersConnected[i]['socket'] == websocket:
				indexPlayerLastCard = i
		lastCard = request['data']['number']
		await jumpToNextPlayer()
	elif request['operation'] == 'turnPassed':
		for player in playersConnected:
			if player['socket'] == websocket:
				player['turnPassed'] = True
		await jumpToNextPlayer()
				
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
