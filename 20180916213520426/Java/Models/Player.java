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

public class Player
{
	private Integer  playerId;
	private String name;
	private Integer  type;
	private Date creationTime;
	
	public Integer  getPlayerId()
	{
		return this.playerId;
	}
	
	public void setPlayerId(Integer  playerId)
	{
		this.playerId = playerId;
	}
	
	public String getName()
	{
		return this.name;
	}
	
	public void setName(String name)
	{
		this.name = name;
	}
	
	public Integer  getType()
	{
		return this.type;
	}
	
	public void setType(Integer  type)
	{
		this.type = type;
	}
	
	public Date getCreationTime()
	{
		return this.creationTime;
	}
	
	public void setCreationTime(Date creationTime)
	{
		this.creationTime = creationTime;
	}
	
	
	public Player(String name, Integer  type)
	{
		this.name = name;
		this.type = type;
	}
	
	public Player()
	{
		this(
			"Test", //Name
			0 //Type
		);
		this.playerId = 0;
		this.creationTime = new Date(0);
	
	}
	

}
