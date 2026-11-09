-- =====================================================================
-- Web Based Hotel Management System - Database Script
-- Tailored to Project Proposal (ESOFT BIT)
-- DBMS: MySQL 8.0
-- Database: hotel_db
-- =====================================================================

CREATE DATABASE IF NOT EXISTS `hotel_db`
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE `hotel_db`;

-- Drop existing tables to allow clean re-import
DROP TABLE IF EXISTS `Bookings`;
DROP TABLE IF EXISTS `Rooms`;
DROP TABLE IF EXISTS `Customers`;

-- 1. Customers Table (Supports Admin, Receptionist, and Customer)
CREATE TABLE `Customers` (
    `CustomerId` INT AUTO_INCREMENT PRIMARY KEY,
    `FullName` VARCHAR(100) NOT NULL,
    `Email` VARCHAR(150) NOT NULL UNIQUE,
    `Password` VARCHAR(255) NOT NULL, -- Stored plain-text per interim demo requirements
    `Phone` VARCHAR(25) NOT NULL,
    `Address` VARCHAR(255) NULL,
    `Role` VARCHAR(20) NOT NULL DEFAULT 'Customer', -- 'Customer', 'Receptionist', 'Admin'
    `CreatedAt` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Rooms Table
CREATE TABLE `Rooms` (
    `RoomId` INT AUTO_INCREMENT PRIMARY KEY,
    `RoomNumber` VARCHAR(20) NOT NULL UNIQUE,
    `RoomType` VARCHAR(50) NOT NULL,
    `PricePerNight` DECIMAL(10, 2) NOT NULL,
    `Capacity` INT NOT NULL DEFAULT 2,
    `Status` VARCHAR(30) NOT NULL DEFAULT 'Available', -- 'Available', 'Maintenance'
    `Description` TEXT NULL,
    `Amenities` VARCHAR(255) NOT NULL DEFAULT 'WiFi, AC, TV',
    `ImageName` VARCHAR(100) NOT NULL DEFAULT 'room_standard.jpg'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Bookings Table (With Room & Customer Relationships)
CREATE TABLE `Bookings` (
    `BookingId` INT AUTO_INCREMENT PRIMARY KEY,
    `CustomerId` INT NOT NULL,
    `RoomId` INT NOT NULL,
    `CheckInDate` DATE NOT NULL,
    `CheckOutDate` DATE NOT NULL,
    `NumberOfGuests` INT NOT NULL DEFAULT 1,
    `TotalAmount` DECIMAL(10, 2) NOT NULL,
    `BookingStatus` VARCHAR(30) NOT NULL DEFAULT 'Confirmed', -- 'Confirmed', 'Cancelled', 'Checked-In', 'Completed'
    `SpecialRequests` TEXT NULL,
    `CreatedAt` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `FK_Bookings_Customers` FOREIGN KEY (`CustomerId`) 
        REFERENCES `Customers` (`CustomerId`) ON DELETE CASCADE,
    CONSTRAINT `FK_Bookings_Rooms` FOREIGN KEY (`RoomId`) 
        REFERENCES `Rooms` (`RoomId`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Indexes for performance and booking lookups
CREATE INDEX `IX_Bookings_Room_Dates` ON `Bookings` (`RoomId`, `CheckInDate`, `CheckOutDate`, `BookingStatus`);
CREATE INDEX `IX_Bookings_Customer` ON `Bookings` (`CustomerId`);

-- =====================================================================
-- Seed Data
-- =====================================================================

-- Users (Admin, Receptionist, Customer)
INSERT INTO `Customers` (`CustomerId`, `FullName`, `Email`, `Password`, `Phone`, `Address`, `Role`) VALUES
(1, 'Pasindu Nirmal Iddamalgoda', 'Pasindu', 'Pasindu@123', '+94778122419', 'Negombo, Sri Lanka', 'Admin'),
(2, 'John Doe', 'john.doe@example.com', 'customer123', '+1 555-0199', '42 Elm Street, Westwood, CA', 'Customer'),
(3, 'Sarah Connor', 'sarah.c@example.com', 'sarah2026', '+1 555-0245', '742 Evergreen Terrace, Springfield', 'Customer'),
(4, 'Elena Rostova', 'reception@hotel.com', 'reception123', '+1 555-0155', 'Front Desk, Luxury Bay Hotel', 'Receptionist');

-- Hotel Rooms (Prices in Sri Lankan Rupees - LKR)
INSERT INTO `Rooms` (`RoomId`, `RoomNumber`, `RoomType`, `PricePerNight`, `Capacity`, `Status`, `Description`, `Amenities`, `ImageName`) VALUES
(1, '101', 'Standard Queen', 28000.00, 2, 'Available', 
 'A cozy, elegant standard room with a plush queen-size bed, ergonomic workstation, and ensuite modern bathroom. Ideal for solo business travelers or couples.', 
 'High-Speed WiFi, Air Conditioning, 43-inch Smart TV, Coffee Maker, Work Desk', 
 'room_standard.jpg'),

(2, '102', 'Deluxe Double', 42000.00, 3, 'Available', 
 'Spacious room featuring two comfortable double beds, panoramic floor-to-ceiling windows, and complimentary morning refreshments.', 
 'High-Speed WiFi, Climate Control, 50-inch 4K TV, Mini Fridge, Safe, Balcony', 
 'room_deluxe.jpg'),

(3, '201', 'Ocean View Suite', 65000.00, 2, 'Available', 
 'Breathtaking coastal views, private sunset balcony, king canopy bed, deep soaking marble tub, and personalized welcome beverage.', 
 'Private Balcony, Ocean View, Mini Bar, Marble Bath, Smart TV, Premium Sound', 
 'room_suite.jpg'),

(4, '202', 'Executive King Suite', 85000.00, 4, 'Available', 
 'Luxury living space featuring a private master bedroom, separate lounge with dining table, kitchenette, and dedicated concierge access.', 
 'Lounge Area, Kitchenette, 65-inch OLED TV, Espresso Machine, King Bed, Jacuzzi', 
 'room_executive.jpg'),

(5, '301', 'Presidential Penthouse', 140000.00, 6, 'Available', 
 'The pinnacle of hospitality. Expansive penthouse with private terrace, personal butler call, grand piano lounge, and jacuzzi.', 
 'Private Terrace, Butler Service, Full Bar, Jacuzzi, Designer Bathrobes, 360 View', 
 'room_presidential.jpg'),

(6, '302', 'Family Villa Suite', 95000.00, 5, 'Available', 
 'Designed for memorable family stays. Two adjoining bedrooms, child-friendly entertainment setup, large living area, and private patio.', 
 '2 Bedrooms, Play Corner, High-Speed WiFi, Microwave, Board Games, Patio', 
 'room_family.jpg');

-- Initial Bookings
INSERT INTO `Bookings` (`BookingId`, `CustomerId`, `RoomId`, `CheckInDate`, `CheckOutDate`, `NumberOfGuests`, `TotalAmount`, `BookingStatus`, `SpecialRequests`) VALUES
(1, 2, 2, '2026-10-10', '2026-10-15', 2, 210000.00, 'Confirmed', 'Late check-in requested around 8:00 PM.'),
(2, 3, 3, '2026-10-12', '2026-10-16', 2, 260000.00, 'Confirmed', 'Extra feather pillows and complimentary wine on arrival.'),
(3, 2, 1, '2026-09-27', '2026-10-02', 2, 140000.00, 'Confirmed', 'Airport shuttle required at 2 PM. Quiet room requested.');
