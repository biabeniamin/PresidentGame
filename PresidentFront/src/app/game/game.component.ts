import { Component, OnInit, Inject, ViewChild, ElementRef } from '@angular/core';
import { DOCUMENT } from '@angular/common';

@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.css']
})
export class GameComponent implements OnInit {

  @ViewChild('popUpWindowContainer2', { static: false }) myDiv: any;
  public displayPopUp : boolean = false;
  public style1 =true;
  public style2 =true;

  constructor(@Inject(DOCUMENT) document)  {
      let popUp = document.getElementById('pop-up-window-container');
      console.log(popUp);
      console.log(this.myDiv);
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
	}

}
