# Challenge SQL/Power BI - Benvenuti a Casa Zanoni

**Exécuter les Requêtes SQL pour Répondre aux Questions**

## Introduction

Ce Challenge ***SQL/Power BI*** analyse les données du restaurant ***Le George***, dirigé par le chef étoilé ***Simone Zanoni***. Il fournit des informations sur les habitudes de visite des clients, le montant total dépensé, et les préférences de menu.

## Instructions

1. Ouvrir ***SQL Server Management Studio (SSMS)***.

2. Se connecter à votre serveur ***SQL Server***.

3. Exécuter le script ***SQL*** suivant pour répondre aux questions :

```sql

-- 1. Quel est le montant total que chaque client a dépensé au restaurant ?

SELECT
    v.id_membre,
    SUM(c.prix) AS montant_total_depense
FROM
    dbo.ventes v
JOIN
    dbo.carte c ON v.id_menu = c.id_menu
GROUP BY
    v.id_membre;
GO

-- 2. Combien de jours chaque client a-t-il visité le restaurant ?

SELECT
    id_membre,
    COUNT(DISTINCT date_visite) AS jours_visites
FROM
    dbo.ventes
GROUP BY
    id_membre;
GO

-- 3. Quel a été le premier menu commandé par chaque client ?

SELECT
    v.id_membre,
    FIRST_VALUE(c.nom_menu) OVER (PARTITION BY v.id_membre ORDER BY v.date_visite) AS premier_menu
FROM
    dbo.ventes v
JOIN
    dbo.carte c ON v.id_menu = c.id_menu
GROUP BY
    v.id_membre, v.date_visite, c.nom_menu;
GO

-- 4. Quel est le menu le plus commandé sur la carte et combien de fois a-t-il été commandé par tous les clients ?

SELECT
    c.nom_menu,
    COUNT(v.id_menu) AS nombre_commandes
FROM
    dbo.ventes v
JOIN
    dbo.carte c ON v.id_menu = c.id_menu
GROUP BY
    c.nom_menu
ORDER BY
    nombre_commandes DESC;
GO

-- 5. Quel menu a été le plus populaire pour chaque client ?

WITH MenuCounts AS (
    SELECT
        v.id_membre,
        c.nom_menu,
        COUNT(v.id_menu) AS nombre_commandes
    FROM
        dbo.ventes v
    JOIN
        dbo.carte c ON v.id_menu = c.id_menu
    GROUP BY
        v.id_membre, c.nom_menu
)
SELECT
    id_membre,
    nom_menu
FROM (
    SELECT
        id_membre,
        nom_menu,
        ROW_NUMBER() OVER (PARTITION BY id_membre ORDER BY nombre_commandes DESC) AS rn
    FROM
        MenuCounts
) AS ranked
WHERE
    rn = 1;
GO

-- 6. Quel menu a été commandé en premier par le client après qu'il soit devenu membre ?

WITH PremierCommande AS (
    SELECT
        v.id_membre,
        MIN(v.date_visite) AS date_premiere_commande
    FROM
        dbo.ventes v
    JOIN
        dbo.membres m ON v.id_membre = m.id_membre
    WHERE
        v.date_visite > m.date_souscription
    GROUP BY
        v.id_membre
)
SELECT
    p.id_membre,
    c.nom_menu
FROM
    PremierCommande p
JOIN
    dbo.ventes v ON p.id_membre = v.id_membre AND p.date_premiere_commande = v.date_visite
JOIN
    dbo.carte c ON v.id_menu = c.id_menu;
GO

-- 7. Quel menu a été commandé juste avant que le client ne devienne membre ?

WITH CommandesAvantAdhesion AS (
    SELECT
        v.id_membre,
        v.id_menu,
        v.date_visite,
        LAG(v.id_menu) OVER (PARTITION BY v.id_membre ORDER BY v.date_visite) AS id_menu_precedent,
        LAG(v.date_visite) OVER (PARTITION BY v.id_membre ORDER BY v.date_visite) AS date_commande_precedente
    FROM
        dbo.ventes v
    JOIN
        dbo.membres m ON v.id_membre = m.id_membre
    WHERE
        v.date_visite < m.date_souscription
)
SELECT
    ca.id_membre,
    c.nom_menu
FROM
    CommandesAvantAdhesion ca
JOIN
    dbo.carte c ON ca.id_menu_precedent = c.id_menu
WHERE
    ca.date_commande_precedente = (
        SELECT MAX(date_commande_precedente)
        FROM CommandesAvantAdhesion
        WHERE id_membre = ca.id_membre
    );

-- 8. Quel est le total des menus et le montant dépensé pour chaque membre avant qu'il ne devienne membre ?

SELECT
    v.id_membre,
    COUNT(v.id_menu) AS total_menus,
    SUM(c.prix) AS montant_total_depense
FROM
    dbo.ventes v
JOIN
    dbo.membres m ON v.id_membre = m.id_membre
JOIN
    dbo.carte c ON v.id_menu = c.id_menu
WHERE
    v.date_visite < m.date_souscription
GROUP BY
    v.id_membre;
GO

-- 9. Si chaque 100 euros dépensés équivalent à 10 points et que les menus dégustation ont un multiplicateur de points de 2x, combien de points chaque client aurait-il ?

WITH Points AS (
    SELECT
        v.id_membre,
        SUM(
            CASE
                WHEN c.nom_menu = 'Menu Dégustation' THEN (c.prix * 2)
                ELSE c.prix
            END
        ) AS total_depenses
    FROM
        dbo.ventes v
    JOIN
        dbo.carte c ON v.id_menu = c.id_menu
    GROUP BY
        v.id_membre
)
SELECT
    id_membre,
    (total_depenses / 100) * 10 AS points_totaux
FROM
    Points;
GO
```