-- Use the appropriate database
USE [challenge_01];
GO

-- Drop tables if they already exist (optional, for re-running the script)
IF OBJECT_ID('dbo.ventes', 'U') IS NOT NULL
    DROP TABLE dbo.ventes;
IF OBJECT_ID('dbo.membres', 'U') IS NOT NULL
    DROP TABLE dbo.membres;
IF OBJECT_ID('dbo.carte', 'U') IS NOT NULL
    DROP TABLE dbo.carte;
GO

-- Création de la table des ventes
CREATE TABLE dbo.ventes (
    id_membre CHAR(1) NOT NULL,
    date_visite DATE NOT NULL,
    id_menu INT NOT NULL,
    PRIMARY KEY (id_membre, date_visite, id_menu)
);
GO

-- Création de la table des membres
CREATE TABLE dbo.membres (
    id_membre CHAR(1) NOT NULL PRIMARY KEY,
    date_souscription DATE NOT NULL
);
GO

-- Création de la table des cartes
CREATE TABLE dbo.carte (
    id_menu INT NOT NULL PRIMARY KEY,
    nom_menu NVARCHAR(50) NOT NULL,
    prix DECIMAL(10, 2) NOT NULL
);
GO

-- Insertion des données dans la table des ventes
INSERT INTO dbo.ventes (id_membre, date_visite, id_menu) VALUES
('A', '2021-01-27', 1),
('A', '2021-02-07', 2),
('A', '2021-03-31', 2),
('A', '2021-04-06', 3),
('A', '2021-04-15', 2),
('B', '2020-11-24', 2),
('B', '2021-02-11', 1),
('B', '2021-06-07', 3),
('B', '2021-08-14', 3),
('B', '2021-09-04', 1),
('C', '2021-02-02', 2),
('C', '2021-05-12', 1),
('C', '2021-06-16', 2);
GO

-- Insertion des données dans la table des membres
INSERT INTO dbo.membres (id_membre, date_souscription) VALUES
('A', '2021-02-08'),
('B', '2021-08-16');
GO

-- Insertion des données dans la table des cartes
INSERT INTO dbo.carte (id_menu, nom_menu, prix) VALUES
(1, 'Menu Déjeuner', 65),
(2, 'Menu Dégustation', 125),
(3, 'Menu Végétarien', 110);
GO
