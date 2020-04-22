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
	public class CardController : ApiController
	{
		// GET cards/values
		public IEnumerable<Card> Get()
		{
			MySqlDataReader reader = new DatabaseOperations().GetReader("SELECT * FROM Cards");
			List<Card> list = new List<Card>();
			
			while(reader.Read())
			{
				list.Add(new Card(
					(int)reader["CardId"],
					(int)reader["PlayerId"],
					(int)reader["Type"],
					(int)reader["Number"],
					(DateTime)reader["CreationTime"]
				));
			}
			
			return list;
		}
		
		// POST cards/values
		public void Post([FromBody]Card data)
		{
			DatabaseOperations db = new DatabaseOperations();
			MySqlCommand command = new MySqlCommand("INSERT INTO Cards(PlayerId,  Type,  Number,  CreationTime) VALUES(@PlayerId,  @Type,  @Number,  @CreationTime)");
			
			command.Parameters.AddWithValue("@PlayerId", data.PlayerId);
			command.Parameters.AddWithValue("@Type", data.Type);
			command.Parameters.AddWithValue("@Number", data.Number);
			command.Parameters.AddWithValue("@CreationTime", DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));
			
			db.ExecuteQuery(command);
		}
		
		// DELETE cards/values/id
		public void Delete(int id)
		{
			DatabaseOperations db = new DatabaseOperations();
			MySqlCommand command = new MySqlCommand("DELETE FROM Cards WHERE CardId=@Id");
			
			command.Parameters.AddWithValue("@Id", id);
			
			db.ExecuteQuery(command);
		}
		
	
	}

}
