# Challenge SQL/Power BI - Benvenuti a Casa Zanoni

**Instructions pour Power BI Desktop**

## Introduction

Ce Challenge ***SQL/Power BI*** analyse les données du restaurant ***Le George***, dirigé par le chef étoilé ***Simone Zanoni***. Il fournit des informations sur les habitudes de visite des clients, le montant total dépensé, et les préférences de menu.

## Structure du Projet

### Fichiers

1. **`create_and_insert_data.sql`**

   - Contient les commandes ***SQL*** pour créer et insérer des données dans les tables de la base de données ***SQL Server***.

2. **Fichier Power BI (`.pbix`)**

   - Contient les rapports et visualisations basés sur les données importées. À créer dans ***Power BI Desktop*** en suivant les instructions ci-dessous.

## Instructions pour SQL Server

### 1. Créer les Tables et Insérer les Données

1. **Ouvrir SQL Server Management Studio (SSMS)**.

2. **Se connecter au serveur SQL Server**.

3. **Exécuter le script SQL suivant pour créer les tables et insérer les données** :

   ```sql
   USE [challenge_01];  -- Sélectionner la base de données à utiliser
   GO

   -- Supprimer les tables si elles existent déjà pour éviter les erreurs
   IF OBJECT_ID('dbo.ventes', 'U') IS NOT NULL
       DROP TABLE dbo.ventes;
   IF OBJECT_ID('dbo.membres', 'U') IS NOT NULL
       DROP TABLE dbo.membres;
   IF OBJECT_ID('dbo.carte', 'U') IS NOT NULL
       DROP TABLE dbo.carte;
   GO

   -- Créer la table 'ventes' pour stocker les informations de commande
   CREATE TABLE dbo.ventes (
       id_membre CHAR(1) NOT NULL,
       date_visite DATE NOT NULL,
       id_menu INT NOT NULL,
       PRIMARY KEY (id_membre, date_visite, id_menu)
   );
   GO

   -- Créer la table 'membres' pour stocker les informations sur les membres
   CREATE TABLE dbo.membres (
       id_membre CHAR(1) NOT NULL PRIMARY KEY,
       date_souscription DATE NOT NULL
   );
   GO

   -- Créer la table 'carte' pour stocker les informations sur les menus
   CREATE TABLE dbo.carte (
       id_menu INT NOT NULL PRIMARY KEY,
       nom_menu NVARCHAR(50) NOT NULL,
       prix DECIMAL(10, 2) NOT NULL
   );
   GO

   -- Insérer les données dans la table 'ventes'
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

   -- Insérer les données dans la table 'membres'
   INSERT INTO dbo.membres (id_membre, date_souscription) VALUES
   ('A', '2021-02-08'),
   ('B', '2021-08-16');
   GO

   -- Insérer les données dans la table 'carte'
   INSERT INTO dbo.carte (id_menu, nom_menu, prix) VALUES
   (1, 'Menu Déjeuner', 65),
   (2, 'Menu Dégustation', 125),
   (3, 'Menu Végétarien', 110);
   GO
   ```


## Instructions pour Power BI

1. Importer les Données

- Ouvrir ***Power BI Desktop***.

- Se connecter à ***SQL Server*** :

- Cliquer sur "Obtenir des données" > "SQL Server".

- Entrer les informations de connexion au serveur ***SQL Server***.

- Sélectionner les tables ventes, membres, et carte.

- Cliquer sur "Charger".

2. Créer les Relations

- Accéder à la vue des relations :

  - Cliquer sur l’icône "Modèle" dans le panneau de gauche.
  - Établir les relations :

  - Faire glisser id_menu de la table ventes vers id_menu de la table carte.
  - Faire glisser id_membre de la table ventes vers id_membre de la table membres.

3. Créer des Mesures et Colonnes Calculées


**Réponses aux Questions:** 

3.1. Montant Total Dépensé :

  - Cliquer sur la table ventes dans le panneau "Champs".

  - Cliquer sur "Nouvelle mesure" dans le menu "Modélisation".

  - Entrer la formule DAX suivante :

    ```DAX
    Montant Total Dépensé = SUMX('ventes', RELATED('carte'[prix]))
    ```

3.2. Nombre de Jours Visités :

  - Cliquer sur "Nouvelle mesure" et entrer la formule :

    ```DAX
    Nombre de Jours Visités = CALCULATE(COUNTROWS(SUMMARIZE('ventes', 'ventes'[id_membre], 'ventes'[date_visite])), ALLEXCEPT('ventes', 'ventes'[id_membre]))
    ```
3.3. Premier Menu Commandé :

  - Cliquer sur "Nouvelle mesure" et entrer la formule :

    ```DAX
    Premier Menu Commandé = CALCULATE(FIRSTNONBLANK('ventes'[id_menu], 1), FILTER('ventes', 'ventes'[date_visite] = MIN('ventes'[date_visite])))
    ```
3.4. Menu le Plus Commandé :

  - Cliquer sur "Nouvelle mesure" et entrer la formule (Créer une Table Résumée pour le Comptage des Commandes) :

    ```DAX
    Nombre_Commandes = COUNTROWS('ventes')
    ```
  - Cliquer sur "Nouvelle mesure" et entrer la formule :   

    ```DAX
    Menu le Plus Commandé = CALCULATE(VALUES('carte'[nom_menu]),TOPN(1,SUMMARIZE('ventes','carte'[nom_menu],"Nombre_Commandes", COUNT('ventes'[id_menu])),[Nombre_Commandes], DESC))
    ```

3.5. Menu Populaire pour Chaque Client :

  - Cliquer sur "Nouvelle mesure" et entrer la formule :

    ```DAX
    Menu Populaire = VAR MenuCounts = SUMMARIZE('ventes', 'ventes'[id_membre], 'ventes'[id_menu], "Nombre_Commandes", COUNT('ventes'[id_menu])) RETURN CALCULATE(FIRSTNONBLANK('carte'[nom_menu], 1), FILTER(MenuCounts, [Nombre_Commandes] = MAXX(FILTER(MenuCounts, 'ventes'[id_membre] = EARLIER('ventes'[id_membre])), [Nombre_Commandes])))
    ```

3.6. Premier Menu Après Adhésion :

  - Cliquer sur "Nouvelle mesure" et entrer la formule :

    ```DAX
    Premier Menu Après Adhésion = CALCULATE(FIRSTNONBLANK('ventes'[id_menu], 1),FILTER('ventes','ventes'[date_visite] > RELATED('membres'[date_souscription])))
    ```
3.7. Menu Avant Adhésion :

  - Cliquer sur "Nouvelle mesure" et entrer la formule :

    ```DAX
    Menu Avant Adhésion = CALCULATE(LASTNONBLANK('ventes'[id_menu], 1),FILTER('ventes','ventes'[date_visite] < RELATED('membres'[date_souscription])))
    ```
3.8. Total Avant Adhésion :

  - Cliquer sur "Nouvelle mesure" et entrer la formule :

   ```DAX
   Total Avant Adhésion = SUMX(FILTER('ventes', 'ventes'[date_visite] < RELATED('membres'[date_souscription])), RELATED('carte'[prix]))
   ```
3.9. Points Totaux :

  - Cliquer sur "Nouvelle mesure" et entrer la formule :

   ```DAX
   Points Totaux = SUMX('ventes', VAR Prix = RELATED('carte'[prix]) RETURN IF(RELATED('carte'[nom_menu]) = "Menu Dégustation", (Prix * 2 / 100) * 10, (Prix / 100) * 10))
   ```


4. Créer des Visualisations

4.1. Ajouter des Visualisations :

Utiliser les types de graphiques comme les histogrammes, les tableaux, et les graphiques en secteurs pour visualiser les données.

4.2. Configurer les Visualisations :

Glisser les mesures et dimensions dans les visualisations pour afficher les résultats.


