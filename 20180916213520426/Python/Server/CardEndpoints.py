#generated automatically
from flask_restful import Resource
from SqlAlchemy import dict_as_obj
from FlaskRestfulHelpers import getArguments
import Card
class CardEndpoints(Resource):
	def __init__(self, **kwargs):
		self.session = kwargs['session']
	
	
	#API endpoints
	#get endpoint
	def get(self):
		requestedArgs = getArguments(['cmd', 'cardId', 'playerId', 'type', 'number', 'creationTime'])
		args  = requestedArgs.parse_args()
		if args['cmd'] == 'getCardsByCardId':
			return Card.getCardsByCardId(self.session, args['cardId'])
		return Card.getCards(self.session)
	
	
	#post endpoint
	def post(self):
		requestedArgs = getArguments(['playerId', 'type', 'number'])
		args  = requestedArgs.parse_args()
		card  = dict_as_obj(args, Card.Card())
		return Card.addCard(self.session, card)
	
	
	#delete endpoint
	def delete(self):
		requestedArgs = getArguments(['cardId'])
		args  = requestedArgs.parse_args()
		return Card.deleteCard(self.session, args['cardId'])
	
	
	#patch endpoint
	def patch(self):
		requestedArgs = getArguments(['cardId', 'playerId', 'type', 'number', 'creationTime'])
		args  = requestedArgs.parse_args()
		card  = Card.getCardsByCardId(self.session, args['cardId'])[0]
		card  = dict_as_obj(args, card)
		return Card.updateCard(self.session, card)
	
	
	

