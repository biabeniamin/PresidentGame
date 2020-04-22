//generated automatically
package com.example.biabe.DatabaseFunctionsGenerator;
import com.example.biabe.DatabaseFunctionsGenerator.Models.*;
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
interface PlayerService
{
	
	@GET("api/players")
	Call<PlayerResponse> getPlayersFiltered(@Query("q") String q);
	@POST("Players.php?cmd=addPlayer")
	Call<Player> addPlayer(@Body Player player);

}

public class Players
{
	public static  getPlayers(Call<> call)
	{
		 players;
		
		players = null;
		
		try
		{
			players = call.execute().body();
		}
		catch(Exception ee)
		{
			System.out.println(ee.getMessage());
		}
		
		return players;
	
	}
	public static  getPlayers()
	{
		 players;
		PlayerService service;
		Call<> call;
		
		players = null;
		
		service = RetrofitInstance.GetRetrofitInstance().create(PlayerService.class);
		try
		{
			call = service.getPlayers();
			players = getPlayers(call);
		}
		catch(Exception ee)
		{
			System.out.println(ee.getMessage());
		}
		
		return players;
	
	}
	
	public static  getPlayersByPlayerId(Integer  playerId)
	{
		 players;
		PlayerService service;
		Call<> call;
		
		players = null;
		
		service = RetrofitInstance.GetRetrofitInstance().create(PlayerService.class);
		try
		{
			call = service.getPlayersByPlayerId(playerId);
			players = getPlayers(call);
		}
		catch(Exception ee)
		{
			System.out.println(ee.getMessage());
		}
		
		return players;
	
	}
	
	
	public static void getPlayers(Call<> call, Callback<> callback)
	{
		try
		{
			call.enqueue(callback);
		}
		catch(Exception ee)
		{
			System.out.println(ee.getMessage());
		}
		
	
	}
	public static void getPlayers(Callback<> callback)
	{
		 players;
		PlayerService service;
		Call<> call;
		
		players = null;
		
		service = RetrofitInstance.GetRetrofitInstance().create(PlayerService.class);
		try
		{
			call = service.getPlayers();
			getPlayers(call, callback);
		}
		catch(Exception ee)
		{
			System.out.println(ee.getMessage());
		}
		
	
	}
	
	public static void getPlayersByPlayerId(Integer  playerId, Callback<> callback)
	{
		 players;
		PlayerService service;
		Call<> call;
		
		players = null;
		
		service = RetrofitInstance.GetRetrofitInstance().create(PlayerService.class);
		try
		{
		);
			getPlayers(call, callback);
		}
		catch(Exception ee)
		{
			System.out.println(ee.getMessage());
		}
		
	
	}
	
	
	public static Player addPlayer(Player player)
	{
		PlayerService service;
		Call<Player> call;
		
		
		service = RetrofitInstance.GetRetrofitInstance().create(PlayerService.class);
		try
		{
			call = service.addPlayer(player);
			player = call.execute().body();
		}
		catch(Exception ee)
		{
			System.out.println(ee.getMessage());
		}
		
		return player;
	
	}
	
	public static void addPlayer(Player player, Callback<Player> callback)
	{
		PlayerService service;
		Call<Player> call;
		
		
		service = RetrofitInstance.GetRetrofitInstance().create(PlayerService.class);
		try
		{
			call = service.addPlayer(player);
			call.enqueue(callback);
		}
		catch(Exception ee)
		{
			System.out.println(ee.getMessage());
		}
	
	}
	

}
