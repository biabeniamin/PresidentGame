import { Component, OnInit, Inject, ViewChild, ElementRef } from '@angular/core';
import { DOCUMENT } from '@angular/common';
import { CardService } from '../CardService';
import { Card } from '../Models/Card';

@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.css']
})
export class GameComponent implements OnInit {

  @ViewChild('popUpWindowContainer2', { static: false }) myDiv: any;
  public displayPopUp : boolean = false;
  public turnRotation : number = 3;
  public playerCards : any;

  constructor(private cardService : CardService)  {
      console.log(this.myDiv);
      cardService.cards.subscribe(data => {
        console.log(data);
        this.playerCards = cardService.cards.getValue().splice(5,3);
        for(let i = 0; i<this.playerCards.length; i++)
        {
          this.playerCards[i].rotation=-68 + 136/(this.playerCards.length - 1) * i;
        }
        console.log(this.playerCards);
      })
   }

  ngOnInit() {
  }
  
  addLocation(event)
	{
    event.preventDefault();
		const target = event.target;
    console.log(this.myDiv);
    console.log(this.myDiv.nativeElement.style);
    //this.myDiv.nativeElement.style["display"] = "none"
    console.log(this.myDiv.nativeElement.style);

    this.displayPopUp = false;
    this.turnRotation++;
	}

}
