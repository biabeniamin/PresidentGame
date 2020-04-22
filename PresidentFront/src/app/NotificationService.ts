import {HttpClient} from '@angular/common/http';
import { ServerUrl } from './ServerUrl'
import { Injectable } from '@angular/core';
import { BehaviorSubject, Subject } from 'rxjs';
import { WebSockets, Message, Request } from './WebSockets';
import { Notification, encodeNotification } from '../app/Models/Notification'

@Injectable({
    providedIn : 'root'
})
export class NotificationService
{
	public notifications : BehaviorSubject<Notification[]>;
	private webSocketsSubject : Subject<Message>;
	GetNotifications()
	{
		return this.http.get<Notification[]>(ServerUrl.GetUrl()  + `Notifications?cmd=get`).subscribe(data =>
		{
			this.notifications.next(data);
		});
	}
	
	static GetDefaultNotification()
	{
		return {
		notificationId : 0,
		title : 'Test',
		message : 'Test',
		creationTime : '2000-01-01 00:00:00'
		};
	}
	
	GetNotificationsByNotificationId(notificationId)
	{
		return this.http.get<Notification[]>(ServerUrl.GetUrl()  + `Notifications?cmd=getNotificationsByNotificationId&notificationId=${notificationId}`);
	}
	
	constructor(private http:HttpClient, private webSockets : WebSockets)
	{
		this.notifications = new BehaviorSubject([NotificationService.GetDefaultNotification()]);
		this.GetNotifications();
		this.webSockets.SetOnConnectionEstablished(() => this.ConnectToWebSockets());
	
	}
	
	AddNotification(notification)
	{
		if (this.webSocketsSubject!=null)
		{
			this.webSocketsSubject.next(new Message(this.constructor.name, new Request('add', 'Notifications', notification)));
			return
		}
		
		return this.http.post<Notification>(ServerUrl.GetUrl()  + `Notifications?cmd=post`, notification).subscribe(notification =>
		{
			console.log(notification);
			if(0 != notification.notificationId)
			{
				let items = this.notifications.getValue()
				items.push(notification)
				this.notifications.next(items)
			}
		});
	}
	
	UpdateNotification(notification)
	{
		if (this.webSocketsSubject!=null)
		{
			this.webSocketsSubject.next(new Message(this.constructor.name, new Request('update', 'Notifications', notification)));
			return
		}
		
		return this.http.patch<Notification>(ServerUrl.GetUrl()  + `Notifications?cmd=updateNotification`, notification).subscribe(notification =>
		{
			console.log(notification);
			return notification;
		});
	}
	
	DeleteNotification(notification)
	{
		if (this.webSocketsSubject!=null)
		{
			this.webSocketsSubject.next(new Message(this.constructor.name, new Request('delete', 'Notifications', notification)));
			return
		}
		
		return this.http.delete<Notification>(ServerUrl.GetUrl()  + `Notifications&cmd=delete&notificationId=` +  notification.notificationId).subscribe(notification =>
		{
			console.log(notification);
			return notification;
		});
	}
	
	ConnectToWebSockets()
	{
		this.webSocketsSubject = this.webSockets.getSubject('Notifications');
		this.webSocketsSubject.subscribe(message =>
		{
				if(message.sender != WebSockets.name)
					return
				let request = message.data;
				console.log(request);
			if(request.operation == 'get')
			{
				this.notifications.next(request.data);
			}
			else if(request.operation == 'add')
			{
				let items = this.notifications.getValue()
				items.push(request.data);
				this.notifications.next(items);
			}
			else if(request.operation == 'update')
			{
				let items = this.notifications.getValue()
				for(let i = 0; i < items.length; i++)
				{
					if(items[i].notificationId == request.data.notificationId)
					{
						items[i] = request.data;
						break;
					}
				}
				this.notifications.next(items);
			}
			else if(request.operation == 'delete')
			{
				let items = this.notifications.getValue()
				for(let i = 0; i < items.length; i++)
				{
					if(items[i].notificationId == request.data.notificationId)
					{
						items.splice(i, 1);
						break;
					}
				}
				this.notifications.next(items);
			}
		
		});
		this.webSocketsSubject.next(new Message(this.constructor.name, new Request('subscribe', 'Notifications', null)));
	}
	

}
