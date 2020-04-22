import { Component, OnInit } from '@angular/core';
import { PlayerService } from '../PlayerService'
import {HttpClient} from '@angular/common/http';
import { FormControl, FormGroup } from '@angular/forms';

@Component({
selector: 'app-player',
templateUrl: './player.component.html',
styleUrls: ['./player.component.css']
})
export class PlayerComponent implements OnInit
{
	
	constructor(private http:HttpClient, 
		private playerService : PlayerService
	)
	{
	
	}
	
	ngOnInit()
	{
	
	}
	
	addPlayer(event)
	{
		event.preventDefault();
		const target = event.target;
		let player = PlayerService.GetDefaultPlayer();
		player.name = target.querySelector('#Name').value;
		player.type = target.querySelector('#Type').value;
		console.log(player);
		this.playerService.AddPlayer(player);
	}
	
	getPlayersByPlayerId(event)
	{
		event.preventDefault();
		const target = event.target;
		let playerId = target.querySelector('#PlayerId').value;
		console.log(playerId);
		this.playerService.GetPlayersByPlayerId(playerId).subscribe(data =>{
			this.playerService.players.next(data);
		});
	}
	
	updateLive(event)
	{
		event.preventDefault();
		const target = event.target;
		this.playerService.ConnectToWebSockets();
	}
	

}

