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
interface CardService
{
	
	@GET("api/cards")
	Call<CardResponse> getCardsFiltered(@Query("q") String q);
	@POST("Cards.php?cmd=addCard")
	Call<Card> addCard(@Body Card card);

}

public class Cards
{
	public static  getCards(Call<> call)
	{
		 cards;
		
		cards = null;
		
		try
		{
			cards = call.execute().body();
		}
		catch(Exception ee)
		{
			System.out.println(ee.getMessage());
		}
		
		return cards;
	
	}
	public static  getCards()
	{
		 cards;
		CardService service;
		Call<> call;
		
		cards = null;
		
		service = RetrofitInstance.GetRetrofitInstance().create(CardService.class);
		try
		{
			call = service.getCards();
			cards = getCards(call);
		}
		catch(Exception ee)
		{
			System.out.println(ee.getMessage());
		}
		
		return cards;
	
	}
	
	public static  getCardsByCardId(Integer  cardId)
	{
		 cards;
		CardService service;
		Call<> call;
		
		cards = null;
		
		service = RetrofitInstance.GetRetrofitInstance().create(CardService.class);
		try
		{
			call = service.getCardsByCardId(cardId);
			cards = getCards(call);
		}
		catch(Exception ee)
		{
			System.out.println(ee.getMessage());
		}
		
		return cards;
	
	}
	
	
	public static void getCards(Call<> call, Callback<> callback)
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
	public static void getCards(Callback<> callback)
	{
		 cards;
		CardService service;
		Call<> call;
		
		cards = null;
		
		service = RetrofitInstance.GetRetrofitInstance().create(CardService.class);
		try
		{
			call = service.getCards();
			getCards(call, callback);
		}
		catch(Exception ee)
		{
			System.out.println(ee.getMessage());
		}
		
	
	}
	
	public static void getCardsByCardId(Integer  cardId, Callback<> callback)
	{
		 cards;
		CardService service;
		Call<> call;
		
		cards = null;
		
		service = RetrofitInstance.GetRetrofitInstance().create(CardService.class);
		try
		{
		);
			getCards(call, callback);
		}
		catch(Exception ee)
		{
			System.out.println(ee.getMessage());
		}
		
	
	}
	
	
	public static Card addCard(Card card)
	{
		CardService service;
		Call<Card> call;
		
		
		service = RetrofitInstance.GetRetrofitInstance().create(CardService.class);
		try
		{
			call = service.addCard(card);
			card = call.execute().body();
		}
		catch(Exception ee)
		{
			System.out.println(ee.getMessage());
		}
		
		return card;
	
	}
	
	public static void addCard(Card card, Callback<Card> callback)
	{
		CardService service;
		Call<Card> call;
		
		
		service = RetrofitInstance.GetRetrofitInstance().create(CardService.class);
		try
		{
			call = service.addCard(card);
			call.enqueue(callback);
		}
		catch(Exception ee)
		{
			System.out.println(ee.getMessage());
		}
	
	}
	

}
