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
class Player(Base):
	@declared_attr
	def __tablename__(cls):
		return 'Players'
	#Fields
	playerId = Column('PlayerId', Integer, primary_key=True)
	name = Column('Name', String(30))
	type = Column('Type', Integer)
	creationTime = Column('CreationTime', DateTime, default=datetime.datetime.utcnow)
	#Foreign Fields
	
	
	#Validation
	@validates('type')
	def validate_type(self, key, value):
		return validate_integer(key, value, False)
	

#Functions

#get funtion
def getPlayers(session):
	result = session.query(Player).all()
	return result


#get dedicated request funtions
def getPlayersByPlayerId(session, playerId):
	result = session.query(Player).filter(Player.playerId == playerId).all()
	return result


#add funtion
def addPlayer(session, player):
	player.creationTime = datetime.datetime.utcnow()
	session.add(player)
	session.commit()
	#this must stay because sqlalchemy query the database because of this line
	print('Value inserted with playerId=', player.playerId)
	return player


#update funtion
def updatePlayer(session, player):
	result = session.query(Player).filter(Player.playerId == player.playerId).first()
	result = player
	session.commit()
	result = session.query(Player).filter(Player.playerId == player.playerId).first()
	return result


#delete funtion
def deletePlayer(session, playerId):
	result = session.query(Player).filter(Player.playerId == playerId).first()
	session.delete(result)
	session.commit()
	return result


def deleteAllPlayer(session, playerId):
	result = session.query(Player).delete()

#API endpoints
#request parser funtion
def getplayerRequestArguments():
	parser = reqparse.RequestParser()
	parser.add_argument('name')
	parser.add_argument('type')
	return parser



