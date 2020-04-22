import { Component, OnInit } from '@angular/core';
import { NotificationService } from '../NotificationService'
import {HttpClient} from '@angular/common/http';
import { FormControl, FormGroup } from '@angular/forms';

@Component({
selector: 'app-notification',
templateUrl: './notification.component.html',
styleUrls: ['./notification.component.css']
})
export class NotificationComponent implements OnInit
{
	
	constructor(private http:HttpClient, 
		private notificationService : NotificationService
	)
	{
	
	}
	
	ngOnInit()
	{
	
	}
	
	addNotification(event)
	{
		event.preventDefault();
		const target = event.target;
		let notification = NotificationService.GetDefaultNotification();
		notification.title = target.querySelector('#Title').value;
		notification.message = target.querySelector('#Message').value;
		console.log(notification);
		this.notificationService.AddNotification(notification);
	}
	
	getNotificationsByNotificationId(event)
	{
		event.preventDefault();
		const target = event.target;
		let notificationId = target.querySelector('#NotificationId').value;
		console.log(notificationId);
		this.notificationService.GetNotificationsByNotificationId(notificationId).subscribe(data =>{
			this.notificationService.notifications.next(data);
		});
	}
	
	updateLive(event)
	{
		event.preventDefault();
		const target = event.target;
		this.notificationService.ConnectToWebSockets();
	}
	

}

