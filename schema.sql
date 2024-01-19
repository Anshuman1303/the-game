create database gamedb;
use gamedb;
CREATE TABLE `userdb` (
  `username` varchar(20) NOT NULL,
  `password` varchar(100) NOT NULL,
  `money` float NOT NULL,
  `admin` varchar(1) DEFAULT 'F',
  `banned` date DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `usermsgs` (
  `sender` varchar(20) NOT NULL,
  `recipient` varchar(20) NOT NULL,
  `message` varchar(1024) NOT NULL,
  `IsRead` varchar(1) DEFAULT 'F',
  `MsgTimeStamp` datetime DEFAULT CURRENT_TIMESTAMP,
  KEY `sender` (`sender`),
  KEY `recipient` (`recipient`),
  CONSTRAINT `usermsgs_ibfk_1` FOREIGN KEY (`sender`) REFERENCES `userdb` (`username`),
  CONSTRAINT `usermsgs_ibfk_2` FOREIGN KEY (`recipient`) REFERENCES `userdb` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
insert into userdb values('admin','admin123',1.175494351E+38,'T',null);
