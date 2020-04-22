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
public class NotificationAdapter extends BaseAdapter
{
	List<Notification> notifications;
	Context context;
	
	@Override
	public int getCount()
	{
		return notifications.size();
	
	}
	
	@Override
	public View getView(int position, View convertView, ViewGroup parent)
	{
		Notification notification;
		TextView notificationIdTextBox;
		TextView titleTextBox;
		TextView messageTextBox;
		TextView creationTimeTextBox;
		
		notification = getItem(position);
		
		if(null == convertView)
		{
			convertView = LayoutInflater.from(context).inflate(R.layout.notification_view, parent, false);
		}
		
		notificationIdTextBox = (TextView) convertView.findViewById(R.id.notificationIdTextBox);
		titleTextBox = (TextView) convertView.findViewById(R.id.titleTextBox);
		messageTextBox = (TextView) convertView.findViewById(R.id.messageTextBox);
		creationTimeTextBox = (TextView) convertView.findViewById(R.id.creationTimeTextBox);
		
		notificationIdTextBox.setText(notification.getNotificationId().toString());
		titleTextBox.setText(notification.getTitle());
		messageTextBox.setText(notification.getMessage());
		creationTimeTextBox.setText(notification.getCreationTime().toString());
		
		return convertView;
	
	}
	
	@Override
	public Notification getItem(int position)
	{
		return notifications.get(position);
	
	}
	
	@Override
	public long getItemId(int position)
	{
		return notifications.get(position).getNotificationId();
	
	}
	
	public NotificationAdapter(List<Notification> notifications, Context context)
	{
		this.notifications = notifications;
		this.context = context;
	
	}
	

}
