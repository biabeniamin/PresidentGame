//generated automatically
using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Web.Http;
using Server.Controllers;
namespace DatabaseFunctionsGenerator
{
	public class NotificationController : ApiController
	{
		// GET notifications/values
		public IEnumerable<Notification> Get()
		{
			MySqlDataReader reader = new DatabaseOperations().GetReader("SELECT * FROM Notifications");
			List<Notification> list = new List<Notification>();
			
			while(reader.Read())
			{
				list.Add(new Notification(
					(int)reader["NotificationId"],
					(string)reader["Title"],
					(string)reader["Message"],
					(DateTime)reader["CreationTime"]
				));
			}
			
			return list;
		}
		
		// POST notifications/values
		public void Post([FromBody]Notification data)
		{
			DatabaseOperations db = new DatabaseOperations();
			MySqlCommand command = new MySqlCommand("INSERT INTO Notifications(Title,  Message,  CreationTime) VALUES(@Title,  @Message,  @CreationTime)");
			
			command.Parameters.AddWithValue("@Title", data.Title);
			command.Parameters.AddWithValue("@Message", data.Message);
			command.Parameters.AddWithValue("@CreationTime", DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));
			
			db.ExecuteQuery(command);
		}
		
		// DELETE notifications/values/id
		public void Delete(int id)
		{
			DatabaseOperations db = new DatabaseOperations();
			MySqlCommand command = new MySqlCommand("DELETE FROM Notifications WHERE NotificationId=@Id");
			
			command.Parameters.AddWithValue("@Id", id);
			
			db.ExecuteQuery(command);
		}
		
	
	}

}
