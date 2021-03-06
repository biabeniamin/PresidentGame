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
  public displayScoreboard : boolean = false;
  public turnRotation : number = 0;
  public playerCards : any[];
  public playerId = 332;
  public playersIndexes = [];
  public lastCard = 0;
  public numberOfCardsSelected = 1;
  public passButtonActivated = false;
  public scoreboard: [];

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
        this.updateCardsClickable();
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

  isCardClickable(card)
  {
    console.log(this.playerCards[this.playersIndexes[0]]);
    let values ={};
    this.playerCards[this.playersIndexes[0]].cards.forEach(card => {
      if(card.number in values)
        values[card.number]++;
      else
        values[card.number] = 1;
    });
    console.log(card.number + " " + this.lastCard);
    return values[card.number] >= this.numberOfCardsSelected && card.number > this.lastCard;
    
  }

  updateCardsClickable()
  {
    this.playerCards[this.playersIndexes[0]].cards.forEach(card => {
      card.isClickable = this.isCardClickable(card);
    });
  }

  cardClicked(card)
  {
    console.log(card);
    if(card.number <= this.lastCard)
      return;
    if(this.turnRotation != 0)
      return;
    let cards = [];
    let cardsAdded = 0;
    for(let i = 0; i< this.playerCards[this.playersIndexes[0]].cards.length;i++)
    {
      let element= this.playerCards[this.playersIndexes[0]].cards[i];
      if(element.number == card.number)
      {
        cards.push(element);
        if(++cardsAdded >= this.numberOfCardsSelected)
          break;
      }
    }
    console.log(cards);
    this.webSockets.Send(new Request('cardSelected', 'Control', {"cards" : cards, "numberOfCards" : this.numberOfCardsSelected}));

  }

  turnPassed()
  {
    if(this.turnRotation != 0)
      return;
    console.log("turn passed");
    this.passButtonActivated = false;
    this.webSockets.Send(new Request('turnPassed', 'Control', ''));
  }

  scoreboardClicked()
  {
    this.displayScoreboard =!this.displayScoreboard;
  }
  
  numberCardsChanged(option)
  {
    if(this.lastCard!=0)
      return;
    this.numberOfCardsSelected = option;
    console.log("cards changed to "+ this.numberOfCardsSelected);
    console.log(option);

    

    this.updateCardsClickable();
    console.log(this.playerCards[this.playersIndexes[0]].cards);
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
        if(this.turnRotation == 2)
          this.turnRotation = 1.6;
        else if(this.turnRotation == 3)
          this.turnRotation = 2.4;
          else if(this.turnRotation == 4)
          this.turnRotation = 2.8;
          else if(this.turnRotation == 5)
          this.turnRotation = 3.4;
        else if(this.turnRotation == 0)
        {
          this.passButtonActivated = true;
        }

          
        this.lastCard = request.data.lastCard;
        this.numberOfCardsSelected = request.data.nrCards;
        console.log("set last card to" + this.lastCard);

        this.updateCardsClickable()
      }
      else if(request.operation == 'scoreboard')
			{
        this.scoreboard = request.data;
      }
		});
	}

}
