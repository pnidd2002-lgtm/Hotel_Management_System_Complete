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

-- Drop existing tables to allow clean re-import (Order matters due to foreign keys!)
DROP TABLE IF EXISTS `Payments`;
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

-- 4. Payments Table (Transaction Ledger & Audit Trail)
CREATE TABLE IF NOT EXISTS `Payments` (
    `PaymentId` INT AUTO_INCREMENT PRIMARY KEY,
    `BookingId` INT NOT NULL,
    `Amount` DECIMAL(18, 2) NOT NULL,
    `PaymentMethod` VARCHAR(50) NOT NULL,
    `TransactionId` VARCHAR(100) NOT NULL,
    `PaymentStatus` VARCHAR(50) NOT NULL,
    `PaymentDate` DATETIME(6) NOT NULL,
    CONSTRAINT `FK_Payments_Bookings_BookingId` FOREIGN KEY (`BookingId`) 
        REFERENCES `Bookings` (`BookingId`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Indexes for performance and booking lookups
CREATE INDEX `IX_Bookings_Room_Dates` ON `Bookings` (`RoomId`, `CheckInDate`, `CheckOutDate`, `BookingStatus`);
CREATE INDEX `IX_Bookings_Customer` ON `Bookings` (`CustomerId`);
CREATE INDEX `IX_Payments_BookingId` ON `Payments` (`BookingId`);

-- =====================================================================
-- Seed Data
-- =====================================================================

-- Users (BCrypt Hashed with workFactor 12: Pasindu@123, customer123, sarah2026, reception123)
INSERT INTO `Customers` (`CustomerId`, `FullName`, `Email`, `Password`, `Phone`, `Address`, `Role`) VALUES
(1, 'Pasindu Nirmal Iddamalgoda', 'Pasindu', '$2a$12$2XO9BU16/z2QyS7vYKsvquv5NNbQBdB/q7DoQ2GPb7fk3RlGDgKca', '+94778122419', 'Negombo, Sri Lanka', 'Admin'),
(2, 'Anuradha', 'anuradha@gmail.com', '$2a$12$DDsgKGf05NvXjjZeir0Y8uB76SLyDJMbcSS/RucZznmV/iMYVMJMm', '+1 555-0199', '42 Elm Street, Westwood, CA', 'Customer'),
(3, 'Sarah Connor', 'sarah.c@example.com', '$2a$12$10GxWzAix/lIDZGdUb/DJeBwqTOkDZbv7MC/mB7OFnQqtxXC7trme', '+1 555-0245', '742 Evergreen Terrace, Springfield', 'Customer'),
(4, 'Elena Rostova', 'reception@hotel.com', '$2a$12$BM2i6TvMs.MVyWoswD7yTeCf1LjBfgxY8IUhuLrAWHf1CZvbAV9ri', '+1 555-0155', 'Front Desk, Luxury Bay Hotel', 'Receptionist');

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

-- Initial Payments (Matching Bookings 1 and 2)
INSERT INTO `Payments` (`PaymentId`, `BookingId`, `Amount`, `PaymentMethod`, `TransactionId`, `PaymentStatus`, `PaymentDate`) VALUES
(1, 1, 210000.00, 'Credit Card (Visa)', 'TXN-20261010-8491A2', 'Completed', '2026-10-10 14:30:00'),
(2, 2, 260000.00, 'Credit Card (Mastercard)', 'TXN-20261012-9214F6', 'Completed', '2026-10-12 09:15:00');
