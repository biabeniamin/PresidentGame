//generated automatically
import { log } from 'util';
import { Injectable } from '@angular/core'
import { Player } from './/Player'
export interface Card
{
	cardId : number;
	playerId : number;
	type : number;
	number : number;
	creationTime : string;
}

export interface CardJSON
{
	playerId : number;
	type : number;
	number : number;
	creationTime : string;
}

export function encodeCard(card: Card): CardJSON {
	return {
		playerId:	card.playerId,
		type:	card.type,
		number:	card.number,
		creationTime:	card.creationTime,
	}
}

