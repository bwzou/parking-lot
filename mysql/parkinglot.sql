-- phpMyAdmin SQL Dump
-- version 4.6.0
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 11, 2016 at 02:15 PM
-- Server version: 5.6.29-log
-- PHP Version: 5.6.20

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `parkinglot`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `order_shift` ()  begin
	DECLARE c_Name varchar(30);
	declare c_PlateNumber varchar(30);
	declare c_Price varchar(30);
	declare c_PayStatus varchar(30);
	declare c_ProduceTime datetime;
	declare c_PID varchar(30);
	declare c_StartTime datetime;
	declare c_EndTime datetime;
	declare c_ID int(11);
	declare b int default 0;
	DECLARE cur_1 CURSOR FOR select `Name`, `PlateNumber`, `Price`, `PayStatus`, `ProduceTime`, `PID`, `StartTime`, `EndTime`, `ID` 	from `order` where `StartTime` + 3000 <= now() and ISNULL(`comeTime`);
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET b = 1;
	OPEN cur_1;
   REPEAT
	FETCH cur_1 INTO c_Name, c_PlateNumber, c_Price, c_PayStatus, c_ProduceTime, c_PID, c_StartTime, c_EndTime, c_ID ;
   INSERT INTO `cancel order`(`Name`, `PlateNumber`, `Price`, `PayStatus`, `ProduceTime`, `PID`, `StartTime`, `EndTime`, `ID`, `cancel_time`)VALUES (c_Name, c_PlateNumber, c_Price, c_PayStatus, c_ProduceTime, c_PID, c_StartTime, c_EndTime, c_ID, now()) ;
   DELETE FROM `order` WHERE `ID` = c_ID ;
	UNTIL b END REPEAT;
	close cur_1;
end$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `cancel order`
--

CREATE TABLE `cancel order` (
  `Name` varchar(30) NOT NULL,
  `PlateNumber` varchar(30) NOT NULL,
  `Price` varchar(30) NOT NULL,
  `PayStatus` varchar(30) NOT NULL DEFAULT '0' COMMENT '1 表示已支付，0表示未支付',
  `ProduceTime` datetime NOT NULL,
  `PID` varchar(30) DEFAULT NULL,
  `StartTime` datetime NOT NULL,
  `EndTime` datetime NOT NULL,
  `ID` int(11) NOT NULL,
  `cancel_time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cancel order`
--

INSERT INTO `cancel order` (`Name`, `PlateNumber`, `Price`, `PayStatus`, `ProduceTime`, `PID`, `StartTime`, `EndTime`, `ID`, `cancel_time`) VALUES
('15602112719', '', '', '0', '2016-05-04 13:20:02', 'A101', '2016-05-04 04:45:00', '2016-05-04 13:45:00', 29, '2016-05-11 21:34:43'),
('15602112719', '', '', '0', '2016-05-04 13:24:27', 'A105', '2016-05-04 01:30:00', '2016-05-04 17:00:00', 30, '2016-05-11 21:34:43'),
('15602112719', '', '', '0', '2016-05-04 15:37:23', 'A102', '2016-05-04 07:00:00', '2016-05-04 15:00:00', 33, '2016-05-11 21:34:43'),
('15602112719', '', '', '0', '2016-05-04 16:16:00', 'A103', '2016-05-04 07:00:00', '2016-05-04 15:15:00', 34, '2016-05-11 21:34:43'),
('111', '', '20', '0', '0000-00-00 00:00:00', 'B102', '2016-05-03 00:00:00', '2016-05-04 00:00:00', 42, '2016-05-11 21:34:43'),
('111', '', '30', '0', '0000-00-00 00:00:00', 'B103', '2016-05-01 00:00:00', '2016-05-02 00:00:00', 43, '2016-05-11 21:34:43'),
('111', '', '24', '0', '2016-05-06 12:04:42', 'A102', '2016-05-06 08:45:00', '2016-05-06 14:45:00', 44, '2016-05-11 21:34:43'),
('111', '', '17', '0', '2016-05-06 14:53:42', 'A101', '2016-05-06 08:15:00', '2016-05-06 12:15:00', 45, '2016-05-11 21:34:43'),
('111', '', '20', '0', '2016-05-06 15:13:12', 'A101', '2016-05-06 11:00:00', '2016-05-06 16:00:00', 48, '2016-05-11 21:34:43'),
('15602112719', '', '14', '0', '2016-05-06 15:20:38', 'A103', '2016-05-06 15:45:00', '2016-05-06 19:15:00', 49, '2016-05-11 21:34:43'),
('111', '', '16', '0', '2016-05-09 18:49:17', 'A101', '2016-05-09 18:45:00', '2016-05-09 22:45:00', 53, '2016-05-11 21:34:43'),
('111', '', '16', '0', '2016-05-09 18:49:24', 'A101', '2016-05-11 18:45:00', '2016-05-11 22:45:00', 54, '2016-05-11 21:34:43'),
('111', '1', '25', '0', '2016-05-09 20:30:32', 'A101', '2016-05-09 10:30:00', '2016-05-09 16:45:00', 56, '2016-05-11 21:34:43'),
('111', '', '20', '0', '2016-05-10 10:11:50', 'A103', '2016-05-11 09:15:00', '2016-05-11 14:15:00', 57, '2016-05-11 21:34:43'),
('111', '2222222', '16', '0', '2016-05-11 00:39:46', 'A101', '2016-05-11 00:30:00', '2016-05-11 04:30:00', 65, '2016-05-11 21:34:43'),
('111', '', '24', '0', '2016-05-11 09:31:43', 'A102', '2016-05-11 08:00:00', '2016-05-11 14:00:00', 66, '2016-05-11 21:34:43'),
('111', '', '16', '0', '2016-05-11 11:12:44', 'A101', '2016-05-11 11:15:00', '2016-05-11 15:15:00', 76, '2016-05-11 21:34:43'),
('15620323783', '', '16', '0', '2016-05-11 11:27:54', 'A103', '2016-05-11 11:30:00', '2016-05-11 15:30:00', 84, '2016-05-11 21:34:43'),
('15620323783', '', '16', '0', '2016-05-11 11:28:00', 'A102', '2016-05-11 11:30:00', '2016-05-11 15:30:00', 85, '2016-05-11 21:34:43'),
('111', '', '21', '0', '2016-05-11 13:30:37', 'A101', '2016-05-11 12:15:00', '2016-05-11 17:30:00', 95, '2016-05-11 21:34:43'),
('111', '123456', '29', '0', '2016-05-11 17:52:52', 'A102', '2016-05-11 14:30:00', '2016-05-11 21:45:00', 96, '2016-05-11 21:34:43'),
('111', '', '16', '0', '2016-05-11 17:54:37', 'A101', '2016-05-11 17:45:00', '2016-05-11 21:45:00', 97, '2016-05-11 21:34:43'),
('111', '', '480', '0', '2016-05-11 19:34:42', 'A103', '2016-05-11 17:30:00', '2016-05-11 23:30:00', 101, '2016-05-11 21:34:43'),
('111', '', '480', '0', '2016-05-11 19:35:38', 'A102', '2016-05-11 17:30:00', '2016-05-11 23:30:00', 102, '2016-05-11 21:34:43');

-- --------------------------------------------------------

--
-- Table structure for table `order`
--

CREATE TABLE `order` (
  `Name` varchar(30) NOT NULL,
  `PlateNumber` varchar(30) NOT NULL,
  `Price` varchar(30) NOT NULL,
  `PayStatus` varchar(30) NOT NULL DEFAULT '0' COMMENT '1 表示已支付，0表示未支付',
  `ProduceTime` datetime NOT NULL,
  `PID` varchar(30) DEFAULT NULL,
  `StartTime` datetime NOT NULL,
  `EndTime` datetime NOT NULL,
  `ID` int(11) NOT NULL,
  `comeTime` datetime DEFAULT NULL,
  `leaveTime` datetime DEFAULT NULL,
  `overpay` int(11) DEFAULT NULL,
  `overpay_state` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `order`
--

INSERT INTO `order` (`Name`, `PlateNumber`, `Price`, `PayStatus`, `ProduceTime`, `PID`, `StartTime`, `EndTime`, `ID`, `comeTime`, `leaveTime`, `overpay`, `overpay_state`) VALUES
('15602112719', '', '', '0', '2016-05-04 12:26:29', 'A102', '2016-05-06 07:00:00', '2016-05-06 17:00:00', 27, '2016-05-11 20:30:44', '2016-05-11 20:32:17', NULL, NULL),
('15602112719', '', '', '0', '2016-05-04 13:15:20', 'A104', '2016-05-04 09:00:00', '2016-05-04 17:00:00', 28, '2016-05-11 20:33:55', '2016-05-11 20:34:10', NULL, NULL),
('111', '', '11', '0', '2016-05-06 18:51:15', 'A102', '2016-05-06 20:00:00', '2016-05-06 22:45:00', 50, '2016-05-11 20:27:58', '2016-05-11 20:28:14', NULL, NULL),
('111', '', '3', '0', '2016-05-06 18:54:53', 'A101', '2016-05-06 22:00:00', '2016-05-06 22:45:00', 51, '2016-05-11 20:26:49', '2016-05-11 20:27:00', NULL, NULL),
('111', '', '72', '0', '2016-05-09 18:43:34', 'A101', '2016-05-10 04:30:00', '2016-05-10 22:30:00', 52, '2016-05-11 20:25:59', '2016-05-11 20:26:09', NULL, NULL),
('111', '', '16', '0', '2016-05-09 19:32:03', 'A102', '2016-05-09 19:30:00', '2016-05-09 23:30:00', 55, '2016-05-11 20:03:25', '2016-05-11 20:03:39', NULL, NULL),
('15620323783', '', '16', '0', '2016-05-10 22:29:26', 'A102', '2016-05-10 19:30:00', '2016-05-10 23:30:00', 59, '2016-05-11 20:19:36', '2016-05-11 20:19:48', NULL, NULL),
('15620323783', '', '76', '0', '2016-05-10 22:29:57', 'A104', '2016-05-10 04:30:00', '2016-05-10 23:30:00', 61, '2016-05-11 20:04:04', '2016-05-11 20:04:15', NULL, NULL),
('15620323783', '', '24', '0', '2016-05-10 22:30:05', 'A103', '2016-05-10 17:30:00', '2016-05-10 23:30:00', 62, '2016-05-11 20:08:02', '2016-05-11 20:08:16', NULL, NULL),
('111', '', '140', '0', '2016-05-10 23:36:19', 'A104', '2016-05-11 22:00:00', '2016-05-11 23:45:00', 63, '2016-05-11 20:16:53', '2016-05-11 20:17:08', NULL, NULL),
('111', '', '12', '0', '2016-05-11 00:31:55', 'A101', '2016-05-11 10:00:00', '2016-05-11 13:00:00', 64, '2016-05-11 11:55:54', '2016-05-11 19:56:58', NULL, NULL),
('111', '', '140', '0', '2016-05-11 20:05:11', 'A104', '2016-05-11 22:00:00', '2016-05-11 23:45:00', 103, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `parkingspace`
--

CREATE TABLE `parkingspace` (
  `ID` varchar(30) NOT NULL,
  `Status` varchar(30) NOT NULL COMMENT '1 表示可用，0表示故障',
  `NowStatus` varchar(30) NOT NULL DEFAULT 'idle' COMMENT 'occupied表示不可用，idle表示空闲，empty表示空',
  `Price` varchar(30) NOT NULL COMMENT '以15分钟时间间隔计费'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `parkingspace`
--

INSERT INTO `parkingspace` (`ID`, `Status`, `NowStatus`, `Price`) VALUES
('A104', '1', 'occupied', ''),
('A101', '1', 'occupied', ''),
('A102', '1', 'occupied', ''),
('A103', '1', 'occupied', ''),
('A105', '1', 'idle', ''),
('B101', '1', 'idle', ''),
('B102', '1', 'occupied', ''),
('B103', '1', 'idle', ''),
('B104', '1', 'idle', ''),
('B105', '1', 'idle', ''),
('C1011', '1', 'idle', '');

-- --------------------------------------------------------

--
-- Table structure for table `price`
--

CREATE TABLE `price` (
  `price` int(11) NOT NULL,
  `changeTime` datetime NOT NULL,
  `type` int(11) NOT NULL COMMENT '0表示正常，1表示罚款，2表示折扣',
  `ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `price`
--

INSERT INTO `price` (`price`, `changeTime`, `type`, `ID`) VALUES
(20, '2016-05-03 08:20:00', 0, 1),
(10, '2016-05-18 07:00:00', 1, 2),
(2, '2016-05-01 08:00:00', 2, 3);

-- --------------------------------------------------------

--
-- Table structure for table `promotion`
--

CREATE TABLE `promotion` (
  `ID` int(11) NOT NULL,
  `title` varchar(50) NOT NULL,
  `content` varchar(500) NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `Name` varchar(30) NOT NULL,
  `Email` varchar(30) DEFAULT NULL,
  `PhoneNumber` varchar(11) DEFAULT NULL,
  `PassWord` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`Name`, `Email`, `PhoneNumber`, `PassWord`) VALUES
('1', 'ffsyzx@126.com', '1', '1'),
('111', '1204073452@qq.com', '111', 'zb'),
('12345', '6543@123.com', '12345', ''),
('12781', 'fia@163.com', '12781', 'zbw'),
('15602112719', 'Jobowen@163.com', '15602112719', '123456'),
('15620323783', 'zuodexin@mail.nankai.edu.cn', '15620323783', '111'),
('222', '1204073452@qq.com', '222', 'zb');

-- --------------------------------------------------------

--
-- Table structure for table `valet`
--

CREATE TABLE `valet` (
  `ID` varchar(30) NOT NULL,
  `Name` varchar(30) NOT NULL,
  `PhoneNumber` varchar(11) NOT NULL,
  `E-mail` varchar(30) NOT NULL,
  `Salary` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cancel order`
--
ALTER TABLE `cancel order`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `order`
--
ALTER TABLE `order`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `price`
--
ALTER TABLE `price`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`Name`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `order`
--
ALTER TABLE `order`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=104;
--
-- AUTO_INCREMENT for table `price`
--
ALTER TABLE `price`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
DELIMITER $$
--
-- Events
--
CREATE DEFINER=`root`@`localhost` EVENT `eventmove` ON SCHEDULE EVERY 1800 SECOND STARTS '2016-05-11 20:34:43' ON COMPLETION PRESERVE ENABLE DO call order_shift()$$

DELIMITER ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
