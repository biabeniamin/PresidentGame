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
	public static class Players
	{
		public static async Task<List<Player>> GetPlayers()
		{
			List<Player> players;
			string data;
			
			players = new List<Player>();
			data = "";
			
			try
			{
				data = await HttpRequestClient.GetRequest("Players.php?cmd=getPlayers");
				players = JsonConvert.DeserializeObject<List<Player>>(data);
			}
			catch(Exception ee)
			{
				Console.WriteLine(ee.Message);
			}
			
			return players;
		
		}
		
		public static async Task<Player> AddPlayer(Player player)
		{
			string data;
			
			data = "";
			
			try
			{
				data = await HttpRequestClient.PostRequest("Players.php?cmd=addPlayer", player);
				player = JsonConvert.DeserializeObject<Player>(data);
			}
			catch(Exception ee)
			{
				Console.WriteLine(ee.Message);
			}
			
			return player;
		
		}
		
	
	}

}
