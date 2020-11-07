#generated automatically
import asyncio
import websockets
import json
from SqlAlchemyMain import session
import CardWebSockets
from CardWebSockets import removeCardsFromPlayer 
from SqlAlchemy import convertToJson, dict_as_obj
import PlayerWebSockets
import NotificationWebSockets
import Player
import Card
from itertools import chain
import time
from WebSocketsHelpers import removeClosedConnectionPlayers

turn = 0
lastCard = 0
indexPlayerLastCard = 0
finishedPlayers = 0
numberOfCardsPerTurn = 1

playersConnected = []
users = set()
def connectedSuccessfullyEvent():
	return json.dumps({'table': 'WebSockets', 'operation' : 'connectedSuccessfully'})

async def removeClosedConnectionPlayersFromGame(session, players):
	print("checking if a player closed the connection")
	for player in players:
		if removeClosedConnectionPlayers(player) == False:
			player["rank"] = 99
			await removeCardsFromPlayer(session, players, player)

async def resetTurnedPassed():
	global playersConnected
	for player in playersConnected:
		player['turnPassed'] = False

async def jumpToNextPlayer():
	global playersConnected, turn, lastCard, indexPlayerLastCard, numberOfCardsPerTurn
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
		cardsCount = {}
		for card in player['cards']:
			if card.number in cardsCount:
				cardsCount[card.number] = cardsCount[card.number] + 1 
			else:
				cardsCount[card.number] = 1
		print("cards count ", cardsCount)
		for card in player['cards']:
			if card.number > lastCard:
				if(int(cardsCount[card.number]) >= int(numberOfCardsPerTurn)):
					foundBigger = True
					print("gasita mai mare la ", card.playerId)
					print("turn", turn, " ", i, " index last player ", indexPlayerLastCard)
					turn = i
					await updateTurn()
					break
	if foundBigger == False:
		#debug only
		print(playersConnected)
		print(turn)
		print(lastCard)
		print(indexPlayerLastCard)
		print(numberOfCardsPerTurn)
		#only to display
		await PlayerWebSockets.setTurn(session, playersConnected, turn, lastCard, numberOfCardsPerTurn)
		lastCard = 0
		turn = indexPlayerLastCard
		numberOfCardsPerTurn = 1
		#reset passed turn
		time.sleep(2)
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
	global turn, playersConnected, lastCard, numberOfCardsPerTurn
	if turn >= len(playersConnected):
		turn = 0
	if len(playersConnected[turn]['cards']) < 1:
		turn = turn + 1
		return await updateTurn()
	print("set turn to ", turn, " and last card to ", lastCard)
	await PlayerWebSockets.setTurn(session, playersConnected, turn, lastCard, numberOfCardsPerTurn)

async def changePresidentCards():
	global playersConnected
	print("changing cards between players")
	sortedPlayers = sorted(playersConnected, key=lambda x: x["lastRank"])
	for card in playersConnected:
		print( "non-sort ",card["lastRank"])
	for card in sortedPlayers:
		print( "sort ",card["lastRank"])
	if len(sortedPlayers) > 1:
		await CardWebSockets.changeCards(session, playersConnected, sortedPlayers[len(sortedPlayers) - 1],sortedPlayers[0], 2)
	if len(sortedPlayers) > 3:
		await CardWebSockets.changeCards(session, playersConnected, sortedPlayers[len(sortedPlayers) - 2],sortedPlayers[1], 1)
	for card in playersConnected[0]["cards"]:
		print( "winner",card.number)
	#playersConnected[0]['cards'],playersConnected[1]['cards']=playersConnected[1]['cards'],playersConnected[0]['cards']
async def startGame(firstTurn = 0):
	global playersSubscribers, turn, playersConnected, lastCard, indexPlayerLastCard, numberOfCardsPerTurn
	Card.deleteAllCards(session)


	index = 0
	while index < len(playersConnected):
		player = playersConnected[index]
		if removeClosedConnectionPlayers(player) == False:
			print("----------------------")
			print("remove player")
			playersConnected.remove(player)
			index = index - 1
			Player.deletePlayer(session, player["player"].playerId)
		index = index + 1
	print("updating players ", len(playersConnected))
	await PlayerWebSockets.updatePlayers(session, playersConnected)
	#Player.deleteAllPlayers(session)
	for player in playersConnected:
		player["cards"] = []
		player["lastRank"] = player["rank"]
		player["rank"] = -1
	await CardWebSockets.shuffleCards(session, playersConnected)
	print(playersConnected)
	turn = firstTurn
	lastCard = 0
	numberOfCardsPerTurn = 1
	await updateTurn()

async def sendScoreboard():
	global playersConnected
	score = []
	for player in playersConnected:
		score.append({"name" : player["player"].name, "score" : player["score"]})
	sortedScore = sorted(score, key=lambda x: x["score"], reverse=True)
	scoreMessage = convertToJson({'operation' : 'scoreboard', 'table' : 'Game', 'data' : sortedScore})
	for player in playersConnected:
		await player['socket'].send(scoreMessage)
	

async def controlRequestReceived(websocket, session, request):
	global playersSubscribers, numberOfCardsPerTurn
	global turn, playersConnected, lastCard, indexPlayerLastCard, finishedPlayers
	#Websockets endpoints
	print("adsdas")
	if request['operation'] == 'start':
		await startGame()
	elif request['operation'] == 'cardSelected':
		await CardWebSockets.cardSelected(session, playersConnected, request['data'])
		numberOfCardsPerTurn = request['data']["numberOfCards"]
		gameOver = False
		indexLooser = -1
		if isGameOver():
			print("game over")
			gameOver = True
		for i in range(0, len(playersConnected)):
			player = playersConnected[i]
			if player['socket'] == websocket:
				indexPlayerLastCard = i
			print('before',player)
			if len(player['cards']) < 1 and player['rank'] == -1:
				player['rank'] = finishedPlayers
				finishedPlayers = finishedPlayers + 1
			print('after',player)
		if gameOver:
			for i in range(0, len(playersConnected)):
				player = playersConnected[i]
				print('before',player)
				if len(player['cards']) > 0:
					player['rank'] = finishedPlayers
					indexLooser = i
					print("setat")
				print('after',player)

		if gameOver == True:
			for player in playersConnected:
				print(player['player'].name, " - ", player['rank'])
			await startGame(indexLooser)
			
			time.sleep(4)
			await changePresidentCards()
			return await sendScoreboard()
		lastCard = request['data']["cards"][0]['number']
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
			global playersConnected
			await removeClosedConnectionPlayersFromGame(session, playersConnected)
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
start_server = websockets.serve(requestReceived, '0.0.0.0', 6789)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
