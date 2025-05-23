-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Creato il: Mag 23, 2025 alle 11:18
-- Versione del server: 10.4.28-MariaDB
-- Versione PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `parcheggio`
--
CREATE DATABASE IF NOT EXISTS `parcheggio` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `parcheggio`;

-- --------------------------------------------------------

--
-- Struttura della tabella `automobili`
--

CREATE TABLE `automobili` (
  `targa` varchar(7) NOT NULL,
  `Data_ingresso` datetime NOT NULL,
  `Data_uscita` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `automobili`
--

INSERT INTO `automobili` (`targa`, `Data_ingresso`, `Data_uscita`) VALUES
('CC345LL', '2025-05-22 08:55:54', NULL);

-- --------------------------------------------------------

--
-- Struttura della tabella `auto_uscite`
--

CREATE TABLE `auto_uscite` (
  `targa` varchar(7) NOT NULL,
  `Data_ingresso` datetime NOT NULL,
  `Data_uscita` datetime NOT NULL,
  `Costo` decimal(10,0) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `auto_uscite`
--

INSERT INTO `auto_uscite` (`targa`, `Data_ingresso`, `Data_uscita`, `Costo`) VALUES
('AA123BB', '2025-05-22 08:55:46', '2025-05-22 10:56:22', 3),
('CC345LL', '2025-05-22 08:19:30', '2025-05-22 10:42:50', 4);

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `automobili`
--
ALTER TABLE `automobili`
  ADD PRIMARY KEY (`targa`);

--
-- Indici per le tabelle `auto_uscite`
--
ALTER TABLE `auto_uscite`
  ADD PRIMARY KEY (`targa`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
