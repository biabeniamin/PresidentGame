import { Component, OnInit, Inject, ViewChild, ElementRef } from '@angular/core';
import { DOCUMENT } from '@angular/common';
import { CardService } from '../CardService';
import { Card } from '../Models/Card';
import { PlayerService } from '../PlayerService';
import { WebSockets, Request, Message } from '../WebSockets';
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
  public playerCards : any[];
  public playerId = 87;
  public playersIndexes = [];
  public lastCard = 0;

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
      playerService.players.subscribe(data => {
        if(data.length < 1)
          return;
        console.log(data);
        this.playerCards = data;
        let hasBeenFounded = false;
         this.playersIndexes = [];
        let order = 0;
        for(let i = 0; i<this.playerCards.length; i++)
        {
          this.playerCards[i].cards = [];
          this.playerCards[i].turn = false;
          if(this.playerCards[i].playerId == this.playerId || hasBeenFounded == true)
          {
            this.playersIndexes.push(i);
            this.playerCards[i].order = order++;
            console.log(this.playersIndexes);
            hasBeenFounded = true;
          }
        }
        //add the beginning
        for(let i = 0; i<this.playerCards.length; i++)
        {
          if(this.playerCards[i].playerId == this.playerId)
          {
            break;
          }
          this.playersIndexes.push(i);
          this.playerCards[i].order = order++;
          console.log(this.playersIndexes);
        }
        console.log(this.playersIndexes);
        console.log(this.playerCards);
        cardService.Subscribe();
        console.log("display cards with id for me:" + this.playerId);
      })
      cardService.cards.subscribe(data => {
        if(data.length < 1)
          return;
        console.log(data);
        console.log(this.playerId)

        //remove old cards from all players
        this.playerCards.forEach(player => {
          player.cards = [];
        })

        data.forEach(card => {
          this.playerCards.forEach(player => {
            if(player.playerId == card.playerId)
              player.cards.push(card);
          });
        });
        console.log(this.playerCards);
        /*this.playerCards = cardService.cards.getValue().filter((card)=>{
          return card.playerId==this.playerId;
        });*/

        for(let j = 0; j<this.playerCards.length; j++)
        {
          let range = 136;
          range=Math.min(range, this.playerCards[j].cards.length * 28)

          for(let i = 0; i<this.playerCards[j].cards.length; i++)
          {
            let card = this.playerCards[j].cards[i];
            card.rotation=-range/2 + range/(this.playerCards[j].cards.length - 1) * i;
            card.class = "card";
            card.class += " "+this.getCardTypeClass(card.type);
            card.class += " "+this.getCardNumberClass(card.number);
          }
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

  cardClicked(card)
  {
    console.log(card);
    if(card.number <= this.lastCard)
      return;
    this.webSockets.Send(new Request('cardSelected', 'Control', card));

  }

  turnPassed()
  {
    console.log("turn passed");
    this.webSockets.Send(new Request('turnPassed', 'Control', ''));
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
        console.log("new id="+this.playerId)
				//this.cards.next(request.data);
      }
      else if(request.operation == 'turn')
			{
        this.playerCards.forEach(element => {
          element.turn = false;
        });

        this.playerCards[request.data.playerIndex].turn = true;
        this.turnRotation = this.playerCards[request.data.playerIndex].order;
        this.lastCard = request.data.lastCard;
        console.log("set last card to" + this.lastCard);
      }
		});
	}

}
