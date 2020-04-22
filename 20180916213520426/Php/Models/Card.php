<?php
//generated automatically
require_once 'Player.php';
class Card
{
	var $cardId;
	var $playerId;
	var $type;
	var $number;
	var $creationTime;
	var $player;

	function GetCardId()
	{
		return $this->cardId;
	}
	function SetCardId($value)
	{
		$this->cardId = $value;
	}
	
	function GetPlayerId()
	{
		return $this->playerId;
	}
	function SetPlayerId($value)
	{
		$this->playerId = $value;
	}
	
	function GetType()
	{
		return $this->type;
	}
	function SetType($value)
	{
		$this->type = $value;
	}
	
	function GetNumber()
	{
		return $this->number;
	}
	function SetNumber($value)
	{
		$this->number = $value;
	}
	
	function GetCreationTime()
	{
		return $this->creationTime;
	}
	function SetCreationTime($value)
	{
		$this->creationTime = $value;
	}
	
	function GetPlayer()
	{
		return $this->player;
	}
	function SetPlayer($value)
	{
		$this->player = $value;
	}
	

	function Card($PlayerId, $Type, $Number)
	{
		$this->cardId = 0;
	
		$this->playerId = $PlayerId;
		$this->type = $Type;
		$this->number = $Number;
	}

}
?>
