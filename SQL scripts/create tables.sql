CREATE TABLE `customers` (
  `CUSTOMERID` varchar(36) NOT NULL,
  `ACTIVATIONDATE` date NOT NULL,
  `DAYSONNETWORK` int NOT NULL,
  `CUMULATIVE30DAYS` int NOT NULL,
  `CUMULATIVE90DAYS` int NOT NULL,
  `LASTRECHARGEDATETIME` datetime NOT NULL,
  `BALANCE` decimal(4,2) NOT NULL,
  PRIMARY KEY (`CUSTOMERID`),
  KEY `Customerid` (`CUSTOMERID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `requestservice` (
  `MESSAGEID` int NOT NULL AUTO_INCREMENT,
  `REQUESTDATETIME` datetime NOT NULL,
  `CUSTOMERID` varchar(36) NOT NULL,
  `REQUESTRESULT` int NOT NULL,
  `REQUESTCONTENT` varchar(100) NOT NULL,
  PRIMARY KEY (`MESSAGEID`)
) ENGINE=InnoDB AUTO_INCREMENT=293501 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `scorringservice` (
  `MESSAGEID` int NOT NULL,
  `CUSTOMERID` varchar(36) NOT NULL,
  `DEBTID` int NOT NULL AUTO_INCREMENT,
  `LOANTYPE` varchar(10) NOT NULL,
  `LOANAMOUNT` decimal(4,2) NOT NULL,
  `RESULTCODE` int NOT NULL,
  `SCORRINGDATETIME` datetime NOT NULL,
  PRIMARY KEY (`DEBTID`)
) ENGINE=InnoDB AUTO_INCREMENT=146317 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `loanprovisionservice` (
  `DEBTID` int NOT NULL,
  `CUSTOMERID` varchar(36) NOT NULL,
  `MESSAGEID` int NOT NULL,
  `LOANDATETIME` datetime NOT NULL,
  `LOANTYPE` varchar(10) NOT NULL,
  `LOANAMOUNT` decimal(4,2) NOT NULL,
  `SERVICEFEE` decimal(4,2) NOT NULL,
  `RESULTCODE` int NOT NULL,
  PRIMARY KEY (`DEBTID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `recharges` (
  `CUSTOMERID` varchar(36) NOT NULL,
  `RECHARGEDATETIME` datetime NOT NULL,
  `RECHARGEAMOUNT` int NOT NULL,
  `MESSAGEID` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`MESSAGEID`)
) ENGINE=InnoDB AUTO_INCREMENT=620902 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `loancollectionservice` (
  `DEBTID` int NOT NULL,
  `COLLECTIONDATETIME` datetime NOT NULL,
  `CUSTOMERID` varchar(36) NOT NULL,
  `MESSAGEID` int NOT NULL,
  `LOANTYPE` varchar(10) NOT NULL,
  `LOANAMOUNT` decimal(4,2) NOT NULL,
  `SERVICEFEE` decimal(4,2) NOT NULL,
  `BALANCE` decimal(4,2) NOT NULL,
  `AMOUNTTOCHARGE` decimal(4,2) NOT NULL,
  `CHARGEDAMOUNT` decimal(4,2) NOT NULL,
  `RESULTCODE` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `loans` (
  `DEBTID` int NOT NULL,
  `CUSTOMERID` varchar(36) NOT NULL,
  `LOANDATETIME` datetime NOT NULL,
  `LOANTYPE` varchar(10) NOT NULL,
  `LOANAMOUNT` decimal(4,2) NOT NULL,
  `SERVICEFEE` decimal(4,2) NOT NULL,
  `PRESENTAMOUNT` decimal(4,2) NOT NULL,
  `LASTCHARGINGATTEMPT` datetime NOT NULL,
  PRIMARY KEY (`DEBTID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `loansarchive` (
  `DEBTID` int NOT NULL,
  `CUSTOMERID` varchar(36) NOT NULL,
  `LOANDATETIME` datetime NOT NULL,
  `LOANTYPE` varchar(10) NOT NULL,
  `LOANAMOUNT` decimal(4,2) NOT NULL,
  `SERVICEFEE` decimal(4,2) NOT NULL,
  `PRESENTAMOUNT` decimal(4,2) NOT NULL,
  `LASTCHARGINGATTEMPT` datetime NOT NULL,
  `ARCHIVEREASON` int NOT NULL,
  `ARCHIVEDATE` datetime NOT NULL,
  PRIMARY KEY (`DEBTID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;




