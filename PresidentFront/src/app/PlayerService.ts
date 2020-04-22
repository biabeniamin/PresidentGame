import {HttpClient} from '@angular/common/http';
import { ServerUrl } from './ServerUrl'
import { Injectable } from '@angular/core';
import { BehaviorSubject, Subject } from 'rxjs';
import { WebSockets, Message, Request } from './WebSockets';
import { Player, encodePlayer } from '../app/Models/Player'

@Injectable({
    providedIn : 'root'
})
export class PlayerService
{
	public players : BehaviorSubject<Player[]>;
	private webSocketsSubject : Subject<Message>;
	GetPlayers()
	{
		return this.http.get<Player[]>(ServerUrl.GetUrl()  + `Players?cmd=get`).subscribe(data =>
		{
			this.players.next(data);
		});
	}
	
	static GetDefaultPlayer()
	{
		return {
		playerId : 0,
		name : 'Test',
		type : 0,
		creationTime : '2000-01-01 00:00:00'
		};
	}
	
	GetPlayersByPlayerId(playerId)
	{
		return this.http.get<Player[]>(ServerUrl.GetUrl()  + `Players?cmd=getPlayersByPlayerId&playerId=${playerId}`);
	}
	
	constructor(private http:HttpClient, private webSockets : WebSockets)
	{
		this.players = new BehaviorSubject([PlayerService.GetDefaultPlayer()]);
		this.GetPlayers();
		this.webSockets.SetOnConnectionEstablished(() => this.ConnectToWebSockets());
	
	}
	
	AddPlayer(player)
	{
		if (this.webSocketsSubject!=null)
		{
			this.webSocketsSubject.next(new Message(this.constructor.name, new Request('add', 'Players', player)));
			return
		}
		
		return this.http.post<Player>(ServerUrl.GetUrl()  + `Players?cmd=post`, player).subscribe(player =>
		{
			console.log(player);
			if(0 != player.playerId)
			{
				let items = this.players.getValue()
				items.push(player)
				this.players.next(items)
			}
		});
	}
	
	UpdatePlayer(player)
	{
		if (this.webSocketsSubject!=null)
		{
			this.webSocketsSubject.next(new Message(this.constructor.name, new Request('update', 'Players', player)));
			return
		}
		
		return this.http.patch<Player>(ServerUrl.GetUrl()  + `Players?cmd=updatePlayer`, player).subscribe(player =>
		{
			console.log(player);
			return player;
		});
	}
	
	DeletePlayer(player)
	{
		if (this.webSocketsSubject!=null)
		{
			this.webSocketsSubject.next(new Message(this.constructor.name, new Request('delete', 'Players', player)));
			return
		}
		
		return this.http.delete<Player>(ServerUrl.GetUrl()  + `Players&cmd=delete&playerId=` +  player.playerId).subscribe(player =>
		{
			console.log(player);
			return player;
		});
	}
	
	ConnectToWebSockets()
	{
		this.webSocketsSubject = this.webSockets.getSubject('Players');
		this.webSocketsSubject.subscribe(message =>
		{
				if(message.sender != WebSockets.name)
					return
				let request = message.data;
				console.log(request);
			if(request.operation == 'get')
			{
				this.players.next(request.data);
			}
			else if(request.operation == 'add')
			{
				let items = this.players.getValue()
				items.push(request.data);
				this.players.next(items);
			}
			else if(request.operation == 'update')
			{
				let items = this.players.getValue()
				for(let i = 0; i < items.length; i++)
				{
					if(items[i].playerId == request.data.playerId)
					{
						items[i] = request.data;
						break;
					}
				}
				this.players.next(items);
			}
			else if(request.operation == 'delete')
			{
				let items = this.players.getValue()
				for(let i = 0; i < items.length; i++)
				{
					if(items[i].playerId == request.data.playerId)
					{
						items.splice(i, 1);
						break;
					}
				}
				this.players.next(items);
			}
		
		});
		this.webSocketsSubject.next(new Message(this.constructor.name, new Request('subscribe', 'Players', null)));
	}
	

}
