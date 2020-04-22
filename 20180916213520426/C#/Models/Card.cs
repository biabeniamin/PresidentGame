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
	public class Card
	{
		private int _cardId;
		private int _playerId;
		private int _type;
		private int _number;
		private DateTime _creationTime;
		private Player _player;
		
		[JsonProperty(PropertyName = "cardId")]
		public int CardId
		{
			get
			{
				return _cardId;
			}
			set
			{
				_cardId = value;
			}
		}
		
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
		
		[JsonProperty(PropertyName = "number")]
		public int Number
		{
			get
			{
				return _number;
			}
			set
			{
				_number = value;
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
		
		[JsonProperty(PropertyName = "player")]
		public Player Player
		{
			get
			{
				return _player;
			}
			set
			{
				_player = value;
			}
		}
		
		
		public Card(int cardId, int playerId, int type, int number, DateTime creationTime)
		{
			_cardId = cardId;
			_playerId = playerId;
			_type = type;
			_number = number;
			_creationTime = creationTime;
		}
		
		public Card(int playerId, int type, int number)
		{
			_playerId = playerId;
			_type = type;
			_number = number;
		}
		
		public Card(int playerId, int type, int number, Player player)
			:this(playerId, type, number)
		{
			_playerId = playerId;
			_type = type;
			_number = number;
		}
		
		public Card()
			 :this(
				0, //PlayerId
				0, //Type
				0 //Number
			)
		{
			_cardId = 0;
			_creationTime = new DateTime(1970, 1, 1, 0, 0, 0);
		}
		
	
	}

}
