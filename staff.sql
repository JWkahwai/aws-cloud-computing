-- --------------------------------------------------------
-- Host:                         staff.cpgv8rvwzl4n.us-east-1.rds.amazonaws.com
-- Server version:               8.0.28 - Source distribution
-- Server OS:                    Linux
-- HeidiSQL Version:             12.3.0.6589
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for staff
CREATE DATABASE IF NOT EXISTS `staff` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `staff`;

-- Dumping structure for table staff.department
CREATE TABLE IF NOT EXISTS `department` (
  `DepartmentID` int NOT NULL,
  `DepartmentName` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`DepartmentID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table staff.department: ~3 rows (approximately)
INSERT INTO `department` (`DepartmentID`, `DepartmentName`) VALUES
	(1, 'HR department'),
	(2, 'Production department'),
	(3, 'Sales department');

-- Dumping structure for table staff.role
CREATE TABLE IF NOT EXISTS `role` (
  `RoleID` int NOT NULL,
  `RoleName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`RoleID`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table staff.role: ~4 rows (approximately)
INSERT INTO `role` (`RoleID`, `RoleName`) VALUES
	(1, 'Director'),
	(2, 'Administrators'),
	(3, 'Manager'),
	(4, 'Staff');

-- Dumping structure for table staff.staff
CREATE TABLE IF NOT EXISTS `staff` (
  `StaffID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL DEFAULT '',
  `Email` varchar(50) NOT NULL DEFAULT '',
  `Phone` varchar(50) NOT NULL DEFAULT '',
  `RoleID` int NOT NULL DEFAULT '0',
  `DepartmentID` int NOT NULL DEFAULT '0',
  `Salary` varchar(50) NOT NULL DEFAULT '',
  `Status` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`StaffID`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table staff.staff: ~3 rows (approximately)
INSERT INTO `staff` (`StaffID`, `Name`, `Email`, `Phone`, `RoleID`, `DepartmentID`, `Salary`, `Status`) VALUES
	(13, 'kahwai', 'kahwaikong123@gmail.com', '0128427621', 3, 1, '12,000', 'Active'),
	(14, 'Gunaseelan', 'Gunaseelan@gmail.com', '0168378825', 1, 1, '8,000', 'Active'),
	(15, 'wei liang', 'weiliang@gmail.com', '0123667982', 2, 1, '6,500', 'Active');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
