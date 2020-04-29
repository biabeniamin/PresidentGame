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
finishedPlayers = 0

playersConnected = []
users = set()
def connectedSuccessfullyEvent():
	return json.dumps({'table': 'WebSockets', 'operation' : 'connectedSuccessfully'})

async def resetTurnedPassed():
	global playersConnected
	for player in playersConnected:
		player['turnPassed'] = False
async def jumpToNextPlayer():
	global playersConnected, turn, lastCard, indexPlayerLastCard
	foundBigger = False
	for i in chain(range(turn + 1, len(playersConnected)), range(0, turn)):
		player = playersConnected[i]
		if player['turnPassed'] == True:
			print("jumped over", player['player'].playerId)
			continue
		if indexPlayerLastCard == i:
			continue
		if foundBigger:
			break
		for card in player['cards']:
			if card.number > lastCard:
				foundBigger = True
				print("gasita mai mare la ", card.playerId)
				print("turn", turn, " ", i, " index last player ", indexPlayerLastCard)
				turn = i
				await updateTurn()
				break
	if foundBigger == False:
		lastCard = 0
		turn = indexPlayerLastCard
		#reset passed turn
		await resetTurnedPassed()
		await updateTurn()

def isGameOver():
	global playersConnected
	remainedPlayers = 0
	for player in playersConnected:
		if len(player['cards']) > 0:
			remainedPlayers = remainedPlayers + 1
	if remainedPlayers < 2:
		return True
	return False

async def updateTurn():
	global turn, playersConnected, lastCard
	if turn >= len(playersConnected):
		turn = 0
	if len(playersConnected[turn]['cards']) < 1:
		turn = turn + 1
		return await updateTurn()
	print("set turn to ", turn, " and last card to ", lastCard)
	await PlayerWebSockets.setTurn(session, playersConnected, turn, lastCard)

async def startGame():
	global playersSubscribers, turn, playersConnected, lastCard, indexPlayerLastCard
	await CardWebSockets.shuffleCards(session, playersConnected)
	print(playersConnected)
	turn = 0
	lastCard = 0
	await updateTurn()

async def controlRequestReceived(websocket, session, request):
	global playersSubscribers
	global turn, playersConnected, lastCard, indexPlayerLastCard, finishedPlayers
	#Websockets endpoints
	print("adsdas")
	if request['operation'] == 'start':
		await startGame()
		#Card.deleteAllCards(session)
		#Player.deleteAllPlayers(session)
	elif request['operation'] == 'cardSelected':
		await CardWebSockets.cardSelected(session, playersConnected, request['data'])
		gameOver = False
		if isGameOver():
			print("game over")
			gameOver = True
		for i in range(0, len(playersConnected)):
			player = playersConnected[i]
			if player['socket'] == websocket:
				indexPlayerLastCard = i
			print(player)
			if len(player['cards']) < 1 and player['rank'] == -1:
				player['rank'] = finishedPlayers
				finishedPlayers = finishedPlayers + 1
			elif len(player['cards']) > 0 and gameOver == True:
				player['rank'] = finishedPlayers
				print("setat")

		if gameOver == True:
			for player in playersConnected:
				print(player['player'].name, " - ", player['rank'])
			return await startGame()
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
