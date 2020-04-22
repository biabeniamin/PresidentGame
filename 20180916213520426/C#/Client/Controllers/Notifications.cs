//generated automatically
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks; 
using Newtonsoft.Json;
namespace DatabaseFunctionsGenerator
{
	public static class Notifications
	{
		public static async Task<List<Notification>> GetNotifications()
		{
			List<Notification> notifications;
			string data;
			
			notifications = new List<Notification>();
			data = "";
			
			try
			{
				data = await HttpRequestClient.GetRequest("Notifications.php?cmd=getNotifications");
				notifications = JsonConvert.DeserializeObject<List<Notification>>(data);
			}
			catch(Exception ee)
			{
				Console.WriteLine(ee.Message);
			}
			
			return notifications;
		
		}
		
		public static async Task<Notification> AddNotification(Notification notification)
		{
			string data;
			
			data = "";
			
			try
			{
				data = await HttpRequestClient.PostRequest("Notifications.php?cmd=addNotification", notification);
				notification = JsonConvert.DeserializeObject<Notification>(data);
			}
			catch(Exception ee)
			{
				Console.WriteLine(ee.Message);
			}
			
			return notification;
		
		}
		
	
	}

}
