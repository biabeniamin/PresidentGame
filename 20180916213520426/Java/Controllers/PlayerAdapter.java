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
public class PlayerAdapter extends BaseAdapter
{
	List<Player> players;
	Context context;
	
	@Override
	public int getCount()
	{
		return players.size();
	
	}
	
	@Override
	public View getView(int position, View convertView, ViewGroup parent)
	{
		Player player;
		TextView playerIdTextBox;
		TextView nameTextBox;
		TextView typeTextBox;
		TextView creationTimeTextBox;
		
		player = getItem(position);
		
		if(null == convertView)
		{
			convertView = LayoutInflater.from(context).inflate(R.layout.player_view, parent, false);
		}
		
		playerIdTextBox = (TextView) convertView.findViewById(R.id.playerIdTextBox);
		nameTextBox = (TextView) convertView.findViewById(R.id.nameTextBox);
		typeTextBox = (TextView) convertView.findViewById(R.id.typeTextBox);
		creationTimeTextBox = (TextView) convertView.findViewById(R.id.creationTimeTextBox);
		
		playerIdTextBox.setText(player.getPlayerId().toString());
		nameTextBox.setText(player.getName());
		typeTextBox.setText(player.getType().toString());
		creationTimeTextBox.setText(player.getCreationTime().toString());
		
		return convertView;
	
	}
	
	@Override
	public Player getItem(int position)
	{
		return players.get(position);
	
	}
	
	@Override
	public long getItemId(int position)
	{
		return players.get(position).getPlayerId();
	
	}
	
	public PlayerAdapter(List<Player> players, Context context)
	{
		this.players = players;
		this.context = context;
	
	}
	

}
