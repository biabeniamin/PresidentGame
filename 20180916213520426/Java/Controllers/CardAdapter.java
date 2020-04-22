//generated automatically
package com.example.biabe.DatabaseFunctionsGenerator;
import com.example.biabe.DatabaseFunctionsGenerator.Models.*;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;
import java.util.List;
public class CardAdapter extends BaseAdapter
{
	List<Card> cards;
	Context context;
	
	@Override
	public int getCount()
	{
		return cards.size();
	
	}
	
	@Override
	public View getView(int position, View convertView, ViewGroup parent)
	{
		Card card;
		TextView cardIdTextBox;
		TextView playerIdTextBox;
		TextView typeTextBox;
		TextView numberTextBox;
		TextView creationTimeTextBox;
		
		card = getItem(position);
		
		if(null == convertView)
		{
			convertView = LayoutInflater.from(context).inflate(R.layout.card_view, parent, false);
		}
		
		cardIdTextBox = (TextView) convertView.findViewById(R.id.cardIdTextBox);
		playerIdTextBox = (TextView) convertView.findViewById(R.id.playerIdTextBox);
		typeTextBox = (TextView) convertView.findViewById(R.id.typeTextBox);
		numberTextBox = (TextView) convertView.findViewById(R.id.numberTextBox);
		creationTimeTextBox = (TextView) convertView.findViewById(R.id.creationTimeTextBox);
		
		cardIdTextBox.setText(card.getCardId().toString());
		playerIdTextBox.setText(card.getPlayerId().toString());
		typeTextBox.setText(card.getType().toString());
		numberTextBox.setText(card.getNumber().toString());
		creationTimeTextBox.setText(card.getCreationTime().toString());
		
		return convertView;
	
	}
	
	@Override
	public Card getItem(int position)
	{
		return cards.get(position);
	
	}
	
	@Override
	public long getItemId(int position)
	{
		return cards.get(position).getCardId();
	
	}
	
	public CardAdapter(List<Card> cards, Context context)
	{
		this.cards = cards;
		this.context = context;
	
	}
	

}
