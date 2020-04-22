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
class Notification(Base):
	@declared_attr
	def __tablename__(cls):
		return 'Notifications'
	#Fields
	notificationId = Column('NotificationId', Integer, primary_key=True)
	title = Column('Title', String(20))
	message = Column('Message', Text)
	creationTime = Column('CreationTime', DateTime, default=datetime.datetime.utcnow)
	#Foreign Fields
	
	
	#Validation
	

#Functions

#get funtion
def getNotifications(session):
	result = session.query(Notification).all()
	return result


#get dedicated request funtions
def getNotificationsByNotificationId(session, notificationId):
	result = session.query(Notification).filter(Notification.notificationId == notificationId).all()
	return result


#add funtion
def addNotification(session, notification):
	notification.creationTime = datetime.datetime.utcnow()
	session.add(notification)
	session.commit()
	#this must stay because sqlalchemy query the database because of this line
	print('Value inserted with notificationId=', notification.notificationId)
	return notification


#update funtion
def updateNotification(session, notification):
	result = session.query(Notification).filter(Notification.notificationId == notification.notificationId).first()
	result = notification
	session.commit()
	result = session.query(Notification).filter(Notification.notificationId == notification.notificationId).first()
	return result


#delete funtion
def deleteNotification(session, notificationId):
	result = session.query(Notification).filter(Notification.notificationId == notificationId).first()
	session.delete(result)
	session.commit()
	return result



#API endpoints
#request parser funtion
def getnotificationRequestArguments():
	parser = reqparse.RequestParser()
	parser.add_argument('title')
	parser.add_argument('message')
	return parser



