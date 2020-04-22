//generated automatically
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks; 
namespace DatabaseFunctionsGenerator
{
	public class Notification
	{
		private int _notificationId;
		private string _title;
		private string _message;
		private DateTime _creationTime;
		
		[JsonProperty(PropertyName = "notificationId")]
		public int NotificationId
		{
			get
			{
				return _notificationId;
			}
			set
			{
				_notificationId = value;
			}
		}
		
		[JsonProperty(PropertyName = "title")]
		public string Title
		{
			get
			{
				return _title;
			}
			set
			{
				_title = value;
			}
		}
		
		[JsonProperty(PropertyName = "message")]
		public string Message
		{
			get
			{
				return _message;
			}
			set
			{
				_message = value;
			}
		}
		
		[JsonProperty(PropertyName = "creationTime")]
		public DateTime CreationTime
		{
			get
			{
				return _creationTime;
			}
			set
			{
				_creationTime = value;
			}
		}
		
		
		public Notification(int notificationId, string title, string message, DateTime creationTime)
		{
			_notificationId = notificationId;
			_title = title;
			_message = message;
			_creationTime = creationTime;
		}
		
		public Notification(string title, string message)
		{
			_title = title;
			_message = message;
		}
		
		public Notification()
			 :this(
				"Test", //Title
				"Test" //Message
			)
		{
			_notificationId = 0;
			_creationTime = new DateTime(1970, 1, 1, 0, 0, 0);
		}
		
	
	}

}
