-- generated by database functions generator automatically
-- for mysql 
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

-- Following lines remove old tables from database
DROP TABLE IF EXISTS`Cards`;
DROP TABLE IF EXISTS`Players`;
DROP TABLE IF EXISTS`Notifications`;

CREATE TABLE `Cards` (
`CardId` INT  NOT NULL,
`PlayerId` INT  NOT NULL,
`Type` INT,
`Number` INT,
`CreationTime` DATETIME  NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE `Cards` ADD PRIMARY KEY(`CardId`); 
ALTER TABLE `Cards`  MODIFY `CardId` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1; 

CREATE TABLE `Players` (
`PlayerId` INT  NOT NULL,
`Name` VARCHAR(30),
`Type` INT,
`CreationTime` DATETIME  NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE `Players` ADD PRIMARY KEY(`PlayerId`); 
ALTER TABLE `Players`  MODIFY `PlayerId` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1; 

CREATE TABLE `Notifications` (
`NotificationId` INT  NOT NULL,
`Title` VARCHAR(20),
`Message` TEXT,
`CreationTime` DATETIME  NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE `Notifications` ADD PRIMARY KEY(`NotificationId`); 
ALTER TABLE `Notifications`  MODIFY `NotificationId` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1; 

