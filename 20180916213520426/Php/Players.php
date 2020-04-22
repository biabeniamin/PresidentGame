<?php
header('Access-Control-Allow-Origin: *'); 
header('Access-Control-Allow-Headers: *'); 
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
$_POST = json_decode(file_get_contents('php://input'), true);
require_once 'Models/Player.php';
require_once 'DatabaseOperations.php';
require_once 'Helpers.php';
function ConvertListToPlayers($data)
{
	$players = [];
	
	foreach($data as $row)
	{
		$player = new Player(
		$row["Name"], 
		$row["Type"] 
		);
	
		$player->SetPlayerId($row["PlayerId"]);
		$player->SetCreationTime($row["CreationTime"]);
	
		$players[count($players)] = $player;
	}
	
	return $players;
}

function GetPlayers($database)
{
	$data = $database->ReadData("SELECT * FROM Players");
	$players = ConvertListToPlayers($data);
	return $players;
}

function GetPlayersByPlayerId($database, $playerId)
{
	$data = $database->ReadData("SELECT * FROM Players WHERE PlayerId = $playerId");
	$players = ConvertListToPlayers($data);
	if(0== count($players))
	{
		return [GetEmptyPlayer()];
	}
	return $players;
}

function CompletePlayers($database, $players)
{
	$playersList = GetPlayers($database);
	foreach($players as $player)
	{
		$start = 0;
		$end = count($playersList) - 1;
		do
		{
	
			$mid = floor(($start + $end) / 2);
			if($player->GetPlayerId() > $playersList[$mid]->GetPlayerId())
			{
				$start = $mid + 1;
			}
			else if($player->GetPlayerId() < $playersList[$mid]->GetPlayerId())
			{
				$end = $mid - 1;
			}
			else if($player->GetPlayerId() == $playersList[$mid]->GetPlayerId())
			{
				$start = $mid + 1;
				$end = $mid - 1;
				$player->SetPlayer($playersList[$mid]);
			}
	
		}while($start <= $end);
	}
	
	return $players;
}

function AddPlayer($database, $player)
{
	$query = "INSERT INTO Players(Name, Type, CreationTime) VALUES(";
	$query = $query . "'" . mysqli_real_escape_string($database->connection ,$player->GetName()) . "', ";
	$query = $query . mysqli_real_escape_string($database->connection ,$player->GetType()).", ";
	$query = $query . "NOW()"."";
	
	$query = $query . ");";
	$database->ExecuteSqlWithoutWarning($query);
	$id = $database->GetLastInsertedId();
	$player->SetPlayerId($id);
	$player->SetCreationTime(date('Y-m-d H:i:s'));
	return $player;
	
}

function DeletePlayer($database, $playerId)
{
	$player = GetPlayersByPlayerId($database, $playerId)[0];
	
	$query = "DELETE FROM Players WHERE PlayerId=$playerId";
	
	$result = $database->ExecuteSqlWithoutWarning($query);
	
	if(0 != $result)
	{
		$player->SetPlayerId(0);
	}
	
	return $player;
	
}

function UpdatePlayer($database, $player)
{
	$query = "UPDATE Players SET ";
	$query = $query . "Name='" . $player->GetName() . "', ";
	$query = $query . "Type=" . $player->GetType()."";
	$query = $query . " WHERE PlayerId=" . $player->GetPlayerId();
	
	$result = $database->ExecuteSqlWithoutWarning($query);
	if(0 == $result)
	{
		$player->SetPlayerId(0);
	}
	return $player;
	
}

function TestAddPlayer($database)
{
	$player = new Player(
		'Test',//Name
		0//Type
	);
	
	AddPlayer($database, $player);
}

function GetEmptyPlayer()
{
	$player = new Player(
		'',//Name
		0//Type
	);
	
	return $player;
}

if(CheckGetParameters(["cmd"]))
{
	if("getPlayers" == $_GET["cmd"])
	{
		$database = new DatabaseOperations();
			echo json_encode(GetPlayers($database));
	}

	if("getLastPlayer" == $_GET["cmd"])
	{
		$database = new DatabaseOperations();
			echo json_encode(GetLastPlayer($database));
	}

	else if("getPlayersByPlayerId" == $_GET["cmd"])
	{
		if(CheckGetParameters([
			'playerId'
			]))
		{
			$database = new DatabaseOperations();
			echo json_encode(GetPlayersByPlayerId($database, 
				$_GET["playerId"]
			));
		}
	
	}

}

if(CheckGetParameters(["cmd"]))
{
	if("addPlayer" == $_GET["cmd"])
	{
		if(CheckPostParameters([
		]))
		{
			$database = new DatabaseOperations();
			$player = new Player(
				IssetValueNull($_POST['name']),
				IssetValueNull($_POST['type'])
			);
	
			echo json_encode(AddPlayer($database, $player));
		}

	}
}

if(CheckGetParameters(["cmd"]))
{
	if("updatePlayer" == $_GET["cmd"])
	{
		$database = new DatabaseOperations();
		$player = new Player(
			$_POST['name'],
			$_POST['type']
		);
		$player->SetPlayerId($_POST['playerId']);
		$player->SetCreationTime($_POST['creationTime']);
		
		$player = UpdatePlayer($database, $player);
		echo json_encode($player);

	}
}

if("DELETE" == $_SERVER['REQUEST_METHOD']
	&& CheckGetParameters(["cmd"]))
{
	if("deletePlayer" == $_GET["cmd"])
	{
		$database = new DatabaseOperations();
		$playerId = $_GET['playerId'];
		
		$player = DeletePlayer($database, $playerId);
		echo json_encode($player);

	}
}


function GetLastPlayer($database)
{
	$data = $database->ReadData("SELECT * FROM Players ORDER BY CreationTime DESC LIMIT 1");
	$players = ConvertListToPlayers($data);
	return $players;
}

?>
