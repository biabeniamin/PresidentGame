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
	public class Player
	{
		private int _playerId;
		private string _name;
		private int _type;
		private DateTime _creationTime;
		
		[JsonProperty(PropertyName = "playerId")]
		public int PlayerId
		{
			get
			{
				return _playerId;
			}
			set
			{
				_playerId = value;
			}
		}
		
		[JsonProperty(PropertyName = "name")]
		public string Name
		{
			get
			{
				return _name;
			}
			set
			{
				_name = value;
			}
		}
		
		[JsonProperty(PropertyName = "type")]
		public int Type
		{
			get
			{
				return _type;
			}
			set
			{
				_type = value;
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
		
		
		public Player(int playerId, string name, int type, DateTime creationTime)
		{
			_playerId = playerId;
			_name = name;
			_type = type;
			_creationTime = creationTime;
		}
		
		public Player(string name, int type)
		{
			_name = name;
			_type = type;
		}
		
		public Player()
			 :this(
				"Test", //Name
				0 //Type
			)
		{
			_playerId = 0;
			_creationTime = new DateTime(1970, 1, 1, 0, 0, 0);
		}
		
	
	}

}
