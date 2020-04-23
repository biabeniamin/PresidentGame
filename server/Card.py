#generated automatically
from sqlalchemy.orm import backref, relationship
from sqlalchemy.orm import validates
from SqlAlchemy import Base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import *
from sqlalchemy.dialects.mysql import DOUBLE
from ValidationError import ValidationError, validate_integer
from flask_restful import reqparse
import datetime
from math import floor
from Player import Player, getPlayers, getPlayersByPlayerId
class Card(Base):
	@declared_attr
	def __tablename__(cls):
		return 'Cards'
	#Fields
	cardId = Column('CardId', Integer, primary_key=True)
	type = Column('Type', Integer)
	number = Column('Number', Integer)
	creationTime = Column('CreationTime', DateTime, default=datetime.datetime.utcnow)
	#Foreign Fields
	playerId = Column('PlayerId', Integer, ForeignKey("Players.PlayerId"))
	players = relationship(Player,backref = backref('cards'))
	player = null
	
	
	#Validation
	@validates('playerId')
	def validate_playerId(self, key, value):
		return validate_integer(key, value, True)
	@validates('type')
	def validate_type(self, key, value):
		return validate_integer(key, value, False)
	@validates('number')
	def validate_number(self, key, value):
		return validate_integer(key, value, False)
	

#Functions
#complete players funtion
def completePlayers(session, cards):
	players = getPlayers(session)
	for row in cards:
		start = 0
		end = len(players)
		while True:
			mid = floor((start + end) / 2)
			if(row.playerId > players[mid].playerId):
				start = mid + 1
			elif(row.playerId < players[mid].playerId):
				end = mid - 1
			elif(row.playerId == players[mid].playerId):
				start = mid + 1
				end = mid - 1
				row.player = players[mid]
			
			if(start > end):
				break
	
	return cards


#get funtion
def getCards(session):
	result = session.query(Card).all()
	result = completePlayers(session, result)
	return result


#get dedicated request funtions
def getCardsByCardId(session, cardId):
	result = session.query(Card).filter(Card.cardId == cardId).all()
	result = completePlayers(session, result)
	return result


#add funtion
def addCard(session, card):
	card.creationTime = datetime.datetime.utcnow()
	session.add(card)
	session.commit()
	#this must stay because sqlalchemy query the database because of this line
	print('Value inserted with cardId=', card.cardId, " and playerId=", card.playerId)
	card.player = getPlayersByPlayerId(session, card.playerId)[0]
	return card


#update funtion
def updateCard(session, card):
	result = session.query(Card).filter(Card.cardId == card.cardId).first()
	result = card
	session.commit()
	result = session.query(Card).filter(Card.cardId == card.cardId).first()
	result.player = getPlayersByPlayerId(session, result.playerId)[0]
	return result


#delete funtion
def deleteCard(session, cardId):
	result = session.query(Card).filter(Card.cardId == cardId).first()
	session.delete(result)
	session.commit()
	return result

def deleteAllCards(session):
	result = session.query(Card).delete()


#API endpoints
#request parser funtion
def getcardRequestArguments():
	parser = reqparse.RequestParser()
	parser.add_argument('playerId')
	parser.add_argument('type')
	parser.add_argument('number')
	return parser



