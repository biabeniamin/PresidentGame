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
	public class PlayerController : ApiController
	{
		// GET players/values
		public IEnumerable<Player> Get()
		{
			MySqlDataReader reader = new DatabaseOperations().GetReader("SELECT * FROM Players");
			List<Player> list = new List<Player>();
			
			while(reader.Read())
			{
				list.Add(new Player(
					(int)reader["PlayerId"],
					(string)reader["Name"],
					(int)reader["Type"],
					(DateTime)reader["CreationTime"]
				));
			}
			
			return list;
		}
		
		// POST players/values
		public void Post([FromBody]Player data)
		{
			DatabaseOperations db = new DatabaseOperations();
			MySqlCommand command = new MySqlCommand("INSERT INTO Players(Name,  Type,  CreationTime) VALUES(@Name,  @Type,  @CreationTime)");
			
			command.Parameters.AddWithValue("@Name", data.Name);
			command.Parameters.AddWithValue("@Type", data.Type);
			command.Parameters.AddWithValue("@CreationTime", DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));
			
			db.ExecuteQuery(command);
		}
		
		// DELETE players/values/id
		public void Delete(int id)
		{
			DatabaseOperations db = new DatabaseOperations();
			MySqlCommand command = new MySqlCommand("DELETE FROM Players WHERE PlayerId=@Id");
			
			command.Parameters.AddWithValue("@Id", id);
			
			db.ExecuteQuery(command);
		}
		
	
	}

}
