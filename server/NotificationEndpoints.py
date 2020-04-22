#generated automatically
from flask_restful import Resource
from SqlAlchemy import dict_as_obj
from FlaskRestfulHelpers import getArguments
import Notification
class NotificationEndpoints(Resource):
	def __init__(self, **kwargs):
		self.session = kwargs['session']
	
	
	#API endpoints
	#get endpoint
	def get(self):
		requestedArgs = getArguments(['cmd', 'notificationId', 'title', 'message', 'creationTime'])
		args  = requestedArgs.parse_args()
		if args['cmd'] == 'getNotificationsByNotificationId':
			return Notification.getNotificationsByNotificationId(self.session, args['notificationId'])
		return Notification.getNotifications(self.session)
	
	
	#post endpoint
	def post(self):
		requestedArgs = getArguments(['title', 'message'])
		args  = requestedArgs.parse_args()
		notification  = dict_as_obj(args, Notification.Notification())
		return Notification.addNotification(self.session, notification)
	
	
	#delete endpoint
	def delete(self):
		requestedArgs = getArguments(['notificationId'])
		args  = requestedArgs.parse_args()
		return Notification.deleteNotification(self.session, args['notificationId'])
	
	
	#patch endpoint
	def patch(self):
		requestedArgs = getArguments(['notificationId', 'title', 'message', 'creationTime'])
		args  = requestedArgs.parse_args()
		notification  = Notification.getNotificationsByNotificationId(self.session, args['notificationId'])[0]
		notification  = dict_as_obj(args, notification)
		return Notification.updateNotification(self.session, notification)
	
	
	

