#generated automatically
from SqlAlchemy import convertToJson, dict_as_obj
from WebSocketsHelpers import checkArguments, removeClosedConnection
import Notification
notificationsSubscribers = set()
async def requestReceived(websocket, session, request):
	global notificationsSubscribers
	#Websockets endpoints
	if request['operation'] == 'get':
		#get endpoint
		notifications = Notification.getNotifications(session)
		response = convertToJson({'operation' : 'get', 'table' : 'Notifications', 'data' : notifications})
		await websocket.send(response)
	
	elif request['operation'] == 'subscribe':
		#subscription endpoint
		notifications = Notification.getNotifications(session)
		response = convertToJson({'operation' : 'get', 'table' : 'Notifications', 'data' : notifications})
		notificationsSubscribers.add(websocket)
		await websocket.send(response)
	
	elif request['operation'] == 'add':
		#add endpoint
		if checkArguments(request, ['title', 'message']) == False:
			print('Not all parameters were provided for ADD in Notifications')
			await websocket.send(convertToJson({'error' : 'Invalid request'}))
			return
		notification = dict_as_obj(request['data'], Notification.Notification(), ['notificationId', 'creationTime'])
		notification = Notification.addNotification(session, notification)
		response = convertToJson({'operation' : 'add', 'table' : 'Notifications', 'data' : notification})
		notificationsSubscribers = set(filter(removeClosedConnection, notificationsSubscribers))
		for subscriber in notificationsSubscribers:
			 await subscriber.send(response)
	
	elif request['operation'] == 'update':
		#update endpoint
		if checkArguments(request, ['notificationId']) == False:
			print('Not all parameters were provided for UPDATE in Notifications')
			await websocket.send(convertToJson({'error' : 'Invalid request'}))
			return
		data = request['data']
		notification = Notification.getNotificationsByNotificationId(session, data['notificationId'])[0]
		notification = dict_as_obj(data, notification)
		notification = Notification.updateNotification(session, notification)
		response = convertToJson({'operation' : 'update', 'table' : 'Notifications', 'data' : notification})
		notificationsSubscribers = set(filter(removeClosedConnection, notificationsSubscribers))
		for subscriber in notificationsSubscribers:
			 await subscriber.send(response)
	
	elif request['operation'] == 'delete':
		#delete endpoint
		if checkArguments(request, ['notificationId']) == False:
			print('Not all parameters were provided for DELETE in Notifications')
			await websocket.send(convertToJson({'error' : 'Invalid request'}))
			return
		notification = Notification.deleteNotification(session, request['data']['notificationId'])
		response = convertToJson({'operation' : 'delete', 'table' : 'Notifications', 'data' : notification})
		notificationsSubscribers = set(filter(removeClosedConnection, notificationsSubscribers))
		for subscriber in notificationsSubscribers:
			 await subscriber.send(response)
	
	

