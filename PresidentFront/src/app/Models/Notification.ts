//generated automatically
import { log } from 'util';
import { Injectable } from '@angular/core'
export interface Notification
{
	notificationId : number;
	title : string;
	message : string;
	creationTime : string;
}

export interface NotificationJSON
{
	title : string;
	message : string;
	creationTime : string;
}

export function encodeNotification(notification: Notification): NotificationJSON {
	return {
		title:	notification.title,
		message:	notification.message,
		creationTime:	notification.creationTime,
	}
}

