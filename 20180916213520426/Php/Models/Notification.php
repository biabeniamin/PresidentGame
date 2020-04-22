<?php
//generated automatically
class Notification
{
	var $notificationId;
	var $title;
	var $message;
	var $creationTime;

	function GetNotificationId()
	{
		return $this->notificationId;
	}
	function SetNotificationId($value)
	{
		$this->notificationId = $value;
	}
	
	function GetTitle()
	{
		return $this->title;
	}
	function SetTitle($value)
	{
		$this->title = $value;
	}
	
	function GetMessage()
	{
		return $this->message;
	}
	function SetMessage($value)
	{
		$this->message = $value;
	}
	
	function GetCreationTime()
	{
		return $this->creationTime;
	}
	function SetCreationTime($value)
	{
		$this->creationTime = $value;
	}
	

	function Notification($Title, $Message)
	{
		$this->notificationId = 0;
	
		$this->title = $Title;
		$this->message = $Message;
	}

}
?>
