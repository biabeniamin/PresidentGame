package com.example.biabe.DatabaseFunctionsGenerator;

import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

public class RetrofitInstance {
    public  static Retrofit GetRetrofitInstance()
    {
        Retrofit retrofit;
        Retrofit.Builder builder;
		Gson gson;

		gson = new GsonBuilder()
                .setDateFormat("yyyy-MM-dd HH:mm:ss")
                .create();

        builder = new Retrofit.Builder()
                .baseUrl("http://192.168.0.100:5000/")
                .addConverterFactory(GsonConverterFactory.create(gson));

        retrofit = builder.build();

        return retrofit;
    }
}
