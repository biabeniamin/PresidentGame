#generated automatically
from flask_restful import Resource
from SqlAlchemy import dict_as_obj
from FlaskRestfulHelpers import getArguments
import Player
class PlayerEndpoints(Resource):
	def __init__(self, **kwargs):
		self.session = kwargs['session']
	
	
	#API endpoints
	#get endpoint
	def get(self):
		requestedArgs = getArguments(['cmd', 'playerId', 'name', 'type', 'creationTime'])
		args  = requestedArgs.parse_args()
		if args['cmd'] == 'getPlayersByPlayerId':
			return Player.getPlayersByPlayerId(self.session, args['playerId'])
		return Player.getPlayers(self.session)
	
	
	#post endpoint
	def post(self):
		requestedArgs = getArguments(['name', 'type'])
		args  = requestedArgs.parse_args()
		player  = dict_as_obj(args, Player.Player())
		return Player.addPlayer(self.session, player)
	
	
	#delete endpoint
	def delete(self):
		requestedArgs = getArguments(['playerId'])
		args  = requestedArgs.parse_args()
		return Player.deletePlayer(self.session, args['playerId'])
	
	
	#patch endpoint
	def patch(self):
		requestedArgs = getArguments(['playerId', 'name', 'type', 'creationTime'])
		args  = requestedArgs.parse_args()
		player  = Player.getPlayersByPlayerId(self.session, args['playerId'])[0]
		player  = dict_as_obj(args, player)
		return Player.updatePlayer(self.session, player)
	
	
	

