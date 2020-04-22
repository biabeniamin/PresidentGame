//generated automatically
package com.example.biabe.DatabaseFunctionsGenerator.Models;
import java.util.List;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
import retrofit2.http.GET;
import retrofit2.http.Query;
import retrofit2.http.POST;
import retrofit2.http.Body;
import java.util.Date;

public class Card
{
	private Integer  cardId;
	private Integer  playerId;
	private Integer  type;
	private Integer  number;
	private Date creationTime;
	private Player player;
	
	public Integer  getCardId()
	{
		return this.cardId;
	}
	
	public void setCardId(Integer  cardId)
	{
		this.cardId = cardId;
	}
	
	public Integer  getPlayerId()
	{
		return this.playerId;
	}
	
	public void setPlayerId(Integer  playerId)
	{
		this.playerId = playerId;
	}
	
	public Integer  getType()
	{
		return this.type;
	}
	
	public void setType(Integer  type)
	{
		this.type = type;
	}
	
	public Integer  getNumber()
	{
		return this.number;
	}
	
	public void setNumber(Integer  number)
	{
		this.number = number;
	}
	
	public Date getCreationTime()
	{
		return this.creationTime;
	}
	
	public void setCreationTime(Date creationTime)
	{
		this.creationTime = creationTime;
	}
	
	public Player getPlayer()
	{
		return this.player;
	}
	
	public void setPlayer(Player player)
	{
		this.player = player;
	}
	
	
	public Card(Integer  playerId, Integer  type, Integer  number)
	{
		this.playerId = playerId;
		this.type = type;
		this.number = number;
	}
	
	public Card(Integer  playerId, Integer  type, Integer  number, Player player)
	{
		this(
			0, //PlayerId
			0, //Type
			0 //Number
		);
		this.player = player;
	
	}
	
	public Card()
	{
		this(
			0, //PlayerId
			0, //Type
			0 //Number
		);
		this.cardId = 0;
		this.creationTime = new Date(0);
	
	}
	

}
