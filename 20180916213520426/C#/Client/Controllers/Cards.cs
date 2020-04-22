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
	public static class Cards
	{
		public static async Task<List<Card>> GetCards()
		{
			List<Card> cards;
			string data;
			
			cards = new List<Card>();
			data = "";
			
			try
			{
				data = await HttpRequestClient.GetRequest("Cards.php?cmd=getCards");
				cards = JsonConvert.DeserializeObject<List<Card>>(data);
			}
			catch(Exception ee)
			{
				Console.WriteLine(ee.Message);
			}
			
			return cards;
		
		}
		
		public static async Task<Card> AddCard(Card card)
		{
			string data;
			
			data = "";
			
			try
			{
				data = await HttpRequestClient.PostRequest("Cards.php?cmd=addCard", card);
				card = JsonConvert.DeserializeObject<Card>(data);
			}
			catch(Exception ee)
			{
				Console.WriteLine(ee.Message);
			}
			
			return card;
		
		}
		
	
	}

}
