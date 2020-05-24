from websockets.protocol import State
def checkArguments(request, arguments):
	print(request)
	print('data' in request)
	if 'data' not in request:
		return False

	for arg in arguments:
		if arg not in request['data']:
			return False
	return True

def removeClosedConnection(item):
	return item.state == State.OPEN 
def removeClosedConnectionPlayers(item):
	return item["socket"].state == State.OPEN 

def filterOpenedConnectionPlayers(players):
	return list(filter(removeClosedConnectionPlayers, players))

def removeClosedConnectionPlayersFromGame(players):
	for player in players:
		if removeClosedConnectionPlayers(player) == False:
			player["rank"] = 99
			player["cards"] = []
