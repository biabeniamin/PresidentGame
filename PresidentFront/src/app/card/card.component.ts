import { Component, OnInit } from '@angular/core';
import { CardService } from '../CardService'
import {HttpClient} from '@angular/common/http';
import { FormControl, FormGroup } from '@angular/forms';
import { PlayerService } from '../PlayerService'
import { WebSockets, Request, Message } from '../WebSockets';

@Component({
selector: 'app-card',
templateUrl: './card.component.html',
styleUrls: ['./card.component.css']
})
export class CardComponent implements OnInit
{
	
	constructor(private http:HttpClient, 
		private cardService : CardService, 
		private playerService : PlayerService,
		private webSockets : WebSockets
	)
	{
	
	}
	
	ngOnInit()
	{
	
	}
	
	addCard(event)
	{
		event.preventDefault();
		const target = event.target;
		let card = CardService.GetDefaultCard();
		card.playerId = target.querySelector('#PlayerIdDropDown').value;
		card.type = target.querySelector('#Type').value;
		card.number = target.querySelector('#Number').value;
		console.log(card);
		this.cardService.AddCard(card);
		
	}
	
	getCardsByCardId(event)
	{
		event.preventDefault();
		const target = event.target;
		let cardId = target.querySelector('#CardId').value;
		console.log(cardId);
		this.cardService.GetCardsByCardId(cardId).subscribe(data =>{
			this.cardService.cards.next(data);
		});
	}
	
	updateLive(event)
	{
		event.preventDefault();
		const target = event.target;
		this.cardService.ConnectToWebSockets();
	}
	
	playerChanged(event)
	{
		console.log(event);
	
	}
	

}

