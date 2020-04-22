<?php
header('Access-Control-Allow-Origin: *'); 
header('Access-Control-Allow-Headers: *'); 
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
$_POST = json_decode(file_get_contents('php://input'), true);
require_once 'Models/Card.php';
require_once 'DatabaseOperations.php';
require_once 'Helpers.php';
require_once 'Players.php';
function ConvertListToCards($data)
{
	$cards = [];
	
	foreach($data as $row)
	{
		$card = new Card(
		$row["PlayerId"], 
		$row["Type"], 
		$row["Number"] 
		);
	
		$card->SetCardId($row["CardId"]);
		$card->SetCreationTime($row["CreationTime"]);
	
		$cards[count($cards)] = $card;
	}
	
	return $cards;
}

function GetCards($database)
{
	$data = $database->ReadData("SELECT * FROM Cards");
	$cards = ConvertListToCards($data);
	$cards = CompletePlayers($database, $cards);
	return $cards;
}

function GetCardsByCardId($database, $cardId)
{
	$data = $database->ReadData("SELECT * FROM Cards WHERE CardId = $cardId");
	$cards = ConvertListToCards($data);
	if(0== count($cards))
	{
		return [GetEmptyCard()];
	}
	CompletePlayers($database, $cards);
	return $cards;
}

function CompleteCards($database, $cards)
{
	$cardsList = GetCards($database);
	foreach($cards as $card)
	{
		$start = 0;
		$end = count($cardsList) - 1;
		do
		{
	
			$mid = floor(($start + $end) / 2);
			if($card->GetCardId() > $cardsList[$mid]->GetCardId())
			{
				$start = $mid + 1;
			}
			else if($card->GetCardId() < $cardsList[$mid]->GetCardId())
			{
				$end = $mid - 1;
			}
			else if($card->GetCardId() == $cardsList[$mid]->GetCardId())
			{
				$start = $mid + 1;
				$end = $mid - 1;
				$card->SetCard($cardsList[$mid]);
			}
	
		}while($start <= $end);
	}
	
	return $cards;
}

function AddCard($database, $card)
{
	$query = "INSERT INTO Cards(PlayerId, Type, Number, CreationTime) VALUES(";
	$query = $query . mysqli_real_escape_string($database->connection ,$card->GetPlayerId()).", ";
	$query = $query . mysqli_real_escape_string($database->connection ,$card->GetType()).", ";
	$query = $query . mysqli_real_escape_string($database->connection ,$card->GetNumber()).", ";
	$query = $query . "NOW()"."";
	
	$query = $query . ");";
	$database->ExecuteSqlWithoutWarning($query);
	$id = $database->GetLastInsertedId();
	$card->SetCardId($id);
	$card->SetCreationTime(date('Y-m-d H:i:s'));
	$card->SetPlayer(GetPlayersByPlayerId($database, $card->GetPlayerId())[0]);
	return $card;
	
}

function DeleteCard($database, $cardId)
{
	$card = GetCardsByCardId($database, $cardId)[0];
	
	$query = "DELETE FROM Cards WHERE CardId=$cardId";
	
	$result = $database->ExecuteSqlWithoutWarning($query);
	
	if(0 != $result)
	{
		$card->SetCardId(0);
	}
	
	return $card;
	
}

function UpdateCard($database, $card)
{
	$query = "UPDATE Cards SET ";
	$query = $query . "PlayerId=" . $card->GetPlayerId().", ";
	$query = $query . "Type=" . $card->GetType().", ";
	$query = $query . "Number=" . $card->GetNumber()."";
	$query = $query . " WHERE CardId=" . $card->GetCardId();
	
	$result = $database->ExecuteSqlWithoutWarning($query);
	if(0 == $result)
	{
		$card->SetCardId(0);
	}
	return $card;
	
}

function TestAddCard($database)
{
	$card = new Card(
		0,//PlayerId
		0,//Type
		0//Number
	);
	
	AddCard($database, $card);
}

function GetEmptyCard()
{
	$card = new Card(
		0,//PlayerId
		0,//Type
		0//Number
	);
	
	return $card;
}

if(CheckGetParameters(["cmd"]))
{
	if("getCards" == $_GET["cmd"])
	{
		$database = new DatabaseOperations();
			echo json_encode(GetCards($database));
	}

	if("getLastCard" == $_GET["cmd"])
	{
		$database = new DatabaseOperations();
			echo json_encode(GetLastCard($database));
	}

	else if("getCardsByCardId" == $_GET["cmd"])
	{
		if(CheckGetParameters([
			'cardId'
			]))
		{
			$database = new DatabaseOperations();
			echo json_encode(GetCardsByCardId($database, 
				$_GET["cardId"]
			));
		}
	
	}

}

if(CheckGetParameters(["cmd"]))
{
	if("addCard" == $_GET["cmd"])
	{
		if(CheckPostParameters([
			'playerId'
		]))
		{
			$database = new DatabaseOperations();
			$card = new Card(
				IssetValueNull($_POST['playerId']),
				IssetValueNull($_POST['type']),
				IssetValueNull($_POST['number'])
			);
	
			echo json_encode(AddCard($database, $card));
		}

	}
}

if(CheckGetParameters(["cmd"]))
{
	if("updateCard" == $_GET["cmd"])
	{
		$database = new DatabaseOperations();
		$card = new Card(
			$_POST['playerId'],
			$_POST['type'],
			$_POST['number']
		);
		$card->SetCardId($_POST['cardId']);
		$card->SetCreationTime($_POST['creationTime']);
		
		$card = UpdateCard($database, $card);
		echo json_encode($card);

	}
}

if("DELETE" == $_SERVER['REQUEST_METHOD']
	&& CheckGetParameters(["cmd"]))
{
	if("deleteCard" == $_GET["cmd"])
	{
		$database = new DatabaseOperations();
		$cardId = $_GET['cardId'];
		
		$card = DeleteCard($database, $cardId);
		echo json_encode($card);

	}
}


function GetLastCard($database)
{
	$data = $database->ReadData("SELECT * FROM Cards ORDER BY CreationTime DESC LIMIT 1");
	$cards = ConvertListToCards($data);
	$cards = CompletePlayers($database, $cards);
	return $cards;
}

?>
