import { Component, OnInit, Inject, ViewChild, ElementRef } from '@angular/core';
import { DOCUMENT } from '@angular/common';
import { CardService } from '../CardService';
import { Card } from '../Models/Card';
import { PlayerService } from '../PlayerService';
import { WebSockets } from '../WebSockets';
import { Subject } from 'rxjs';

@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.css']
})
export class GameComponent implements OnInit {

  @ViewChild('popUpWindowContainer2', { static: false }) myDiv: any;
  public displayPopUp : boolean = true;
  public turnRotation : number = 3;
  public playerCards : any;
  public playerId = 3;

  private webSocketsSubject : Subject<any>;

  getCardTypeClass(type : number) : string
  {
    switch(type)
    {
      case 0:
        return "schelle";
      case 1:
        return "eichel";
      case 2:
        return "roesle";
      case 3:
        return "schilte";
    }

    return "";
  }

  getCardNumberClass(type : number) : string
  {
    switch(type)
    {
      case 2:
        return "two";
      case 3:
        return "three";
        case 4:
          return "four";
        case 5:
          return "five";
        case 6:
          return "six";
        case 7:
          return "seven";
          case 8:
            return "eight";
            case 9:
              return "nine";
            case 10:
              return "ten";
            case 11:
              return "jack";
        case 12:
            return "queen";
          case 13:
            return "king";
          case 14:
            return "ace";
    }

    return "";
  }

  constructor(private cardService : CardService, private playerService : PlayerService, private webSockets : WebSockets)  {
      console.log(this.myDiv);
      cardService.cards.subscribe(data => {
        console.log(data);
        this.playerCards = cardService.cards.getValue().filter((card)=>{
          return card.player.type==this.playerId;
        });

        let range = 136;
        range=Math.min(range, this.playerCards.length * 28)

        for(let i = 0; i<this.playerCards.length; i++)
        {
          let card = this.playerCards[i];
          card.rotation=-range/2 + range/(this.playerCards.length - 1) * i;
          card.class = "card";
          card.class += " "+this.getCardTypeClass(card.type);
          card.class += " "+this.getCardNumberClass(card.number);
        }
        console.log(this.playerCards);
      })

      this.webSockets.SetOnConnectionEstablished(() => this.ConnectToWebSockets());
   }

  ngOnInit() {
  }
  
  addPlayer(event)
	{
    event.preventDefault();
		const target = event.target;
		let player = PlayerService.GetDefaultPlayer();
    player.name = target.querySelector('#Name').value;
    player.type = 2;
		console.log(player);
		this.playerService.AddPlayer(player);
  }
  
  ConnectToWebSockets()
	{
		this.webSocketsSubject = this.webSockets.getSubject('Game');
		this.webSocketsSubject.subscribe(message =>
		{
				if(message.sender != WebSockets.name)
					return
				let request = message.data;
				console.log(request);
			if(request.operation == 'registered')
			{
        this.displayPopUp = false;
        this.playerId = request.data.playerId;
				//this.cards.next(request.data);
			}
		});
	}

}
