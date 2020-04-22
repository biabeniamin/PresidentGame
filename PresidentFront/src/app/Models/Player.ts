//generated automatically
import { log } from 'util';
import { Injectable } from '@angular/core'
export interface Player
{
	playerId : number;
	name : string;
	type : number;
	creationTime : string;
}

export interface PlayerJSON
{
	name : string;
	type : number;
	creationTime : string;
}

export function encodePlayer(player: Player): PlayerJSON {
	return {
		name:	player.name,
		type:	player.type,
		creationTime:	player.creationTime,
	}
}

