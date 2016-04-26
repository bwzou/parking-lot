-- phpMyAdmin SQL Dump
-- version 4.5.4.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: 2016-04-22 15:49:08
-- 服务器版本： 5.7.10-log
-- PHP Version: 7.0.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `parkinglot`
--

-- --------------------------------------------------------

--
-- 表的结构 `orders`
--

CREATE TABLE `orders` (
  `Name` varchar(30) NOT NULL,
  `PlateNumber` varchar(30) DEFAULT NULL,
  `Price` int(10) DEFAULT NULL,
  `PayStatus` int(10) NOT NULL DEFAULT '0',
  `ProduceTime` datetime NOT NULL,
  `StartTime` datetime NOT NULL,
  `EndTime` datetime NOT NULL,
  `LotID` varchar(30) DEFAULT NULL,
  `ID` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `parkingspace`
--

CREATE TABLE `parkingspace` (
  `ID` varchar(30) NOT NULL,
  `Status` varchar(30) NOT NULL,
  `Price` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `user`
--

CREATE TABLE `user` (
  `ID` varchar(30) NOT NULL,
  `Name` varchar(30) DEFAULT NULL,
  `E-mail` varchar(30) NOT NULL,
  `PhoneNumber` varchar(30) NOT NULL,
  `PassWord` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `valet`
--

CREATE TABLE `valet` (
  `ID` varchar(30) NOT NULL,
  `Name` varchar(30) NOT NULL,
  `PhoneNumber` varchar(30) NOT NULL,
  `E-mail` varchar(30) NOT NULL,
  `Salary` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `FK_ID` (`LotID`);

--
-- Indexes for table `parkingspace`
--
ALTER TABLE `parkingspace`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `valet`
--
ALTER TABLE `valet`
  ADD PRIMARY KEY (`ID`);

--
-- 限制导出的表
--

--
-- 限制表 `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `FK_ID` FOREIGN KEY (`LotID`) REFERENCES `parkingspace` (`ID`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
