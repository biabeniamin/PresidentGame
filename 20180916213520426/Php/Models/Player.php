<?php
//generated automatically
class Player
{
	var $playerId;
	var $name;
	var $type;
	var $creationTime;

	function GetPlayerId()
	{
		return $this->playerId;
	}
	function SetPlayerId($value)
	{
		$this->playerId = $value;
	}
	
	function GetName()
	{
		return $this->name;
	}
	function SetName($value)
	{
		$this->name = $value;
	}
	
	function GetType()
	{
		return $this->type;
	}
	function SetType($value)
	{
		$this->type = $value;
	}
	
	function GetCreationTime()
	{
		return $this->creationTime;
	}
	function SetCreationTime($value)
	{
		$this->creationTime = $value;
	}
	

	function Player($Name, $Type)
	{
		$this->playerId = 0;
	
		$this->name = $Name;
		$this->type = $Type;
	}

}
?>
