import {HttpClient} from '@angular/common/http';
import { ServerUrl } from './ServerUrl'
import { Injectable } from '@angular/core';
import { BehaviorSubject, Subject } from 'rxjs';
import { WebSockets, Message, Request } from './WebSockets';
import { Card, encodeCard } from '../app/Models/Card'
import { Player } from '../app/Models/Player'
import { PlayerService } from './PlayerService'

@Injectable({
    providedIn : 'root'
})
export class CardService
{
	public cards : BehaviorSubject<Card[]>;
	private webSocketsSubject : Subject<Message>;
	GetCards()
	{
		return this.http.get<Card[]>(ServerUrl.GetUrl()  + `Cards?cmd=get`).subscribe(data =>
		{
			this.cards.next(data);
		});
	}
	
	static GetDefaultCard()
	{
		return {
		cardId : 0,
		playerId : 0,
		type : 0,
		number : 0,
		creationTime : '2000-01-01 00:00:00',
		player : PlayerService.GetDefaultPlayer()
		};
	}
	
	GetCardsByCardId(cardId)
	{
		return this.http.get<Card[]>(ServerUrl.GetUrl()  + `Cards?cmd=getCardsByCardId&cardId=${cardId}`);
	}
	
	constructor(private http:HttpClient, private webSockets : WebSockets)
	{
		this.cards = new BehaviorSubject([CardService.GetDefaultCard()]);
		this.GetCards();
		this.webSockets.SetOnConnectionEstablished(() => this.ConnectToWebSockets());
	
	}
	
	AddCard(card)
	{
		if (this.webSocketsSubject!=null)
		{
			this.webSocketsSubject.next(new Message(this.constructor.name, new Request('add', 'Cards', card)));
			return
		}
		
		return this.http.post<Card>(ServerUrl.GetUrl()  + `Cards?cmd=post`, card).subscribe(card =>
		{
			console.log(card);
			if(0 != card.cardId)
			{
				let items = this.cards.getValue()
				items.push(card)
				this.cards.next(items)
			}
		});
	}
	
	UpdateCard(card)
	{
		if (this.webSocketsSubject!=null)
		{
			this.webSocketsSubject.next(new Message(this.constructor.name, new Request('update', 'Cards', card)));
			return
		}
		
		return this.http.patch<Card>(ServerUrl.GetUrl()  + `Cards?cmd=updateCard`, card).subscribe(card =>
		{
			console.log(card);
			return card;
		});
	}
	
	DeleteCard(card)
	{
		if (this.webSocketsSubject!=null)
		{
			this.webSocketsSubject.next(new Message(this.constructor.name, new Request('delete', 'Cards', card)));
			return
		}
		
		return this.http.delete<Card>(ServerUrl.GetUrl()  + `Cards&cmd=delete&cardId=` +  card.cardId).subscribe(card =>
		{
			console.log(card);
			return card;
		});
	}
	
	ConnectToWebSockets()
	{
		this.webSocketsSubject = this.webSockets.getSubject('Cards');
		this.webSocketsSubject.subscribe(message =>
		{
				if(message.sender != WebSockets.name)
					return
				let request = message.data;
				console.log(request);
			if(request.operation == 'get')
			{
				this.cards.next(request.data);
			}
			else if(request.operation == 'add')
			{
				let items = this.cards.getValue()
				items.push(request.data);
				this.cards.next(items);
			}
			else if(request.operation == 'update')
			{
				let items = this.cards.getValue()
				for(let i = 0; i < items.length; i++)
				{
					if(items[i].cardId == request.data.cardId)
					{
						items[i] = request.data;
						break;
					}
				}
				this.cards.next(items);
			}
			else if(request.operation == 'delete')
			{
				let items = this.cards.getValue()
				for(let i = 0; i < items.length; i++)
				{
					if(items[i].cardId == request.data.cardId)
					{
						items.splice(i, 1);
						break;
					}
				}
				this.cards.next(items);
			}
		
		});
		this.webSocketsSubject.next(new Message(this.constructor.name, new Request('subscribe', 'Cards', null)));
	}
	

}
