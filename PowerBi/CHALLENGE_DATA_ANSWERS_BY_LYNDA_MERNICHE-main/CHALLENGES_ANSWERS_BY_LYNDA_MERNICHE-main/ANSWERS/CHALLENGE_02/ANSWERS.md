# Challenge SQL/Power BI - The Agency

## Introduction

Ce challenge vise à améliorer l'expérience client de ***Stéphane*** et ***Alex***, deux agents immobiliers, en utilisant des données sur les loyers. Ce document décrit le processus de traitement des données, y compris la création d'un schéma de données, le nettoyage, l'analyse exploratoire, et la mise en place d'un pipeline de données en temps réel.

## 1. Proposition de Schéma Significatif

Pour organiser les données de manière efficace, nous avons défini trois tables principales :

### Table des Logements

| Colonne                  | Description                                    |
|--------------------------|------------------------------------------------|
| `id_logement`            | Identifiant unique pour chaque logement       |
| `type_habitat`           | Type de logement (ex. appartement, maison)    |
| `epoque_construction`    | Époque de construction (ex. années 60, années 2000) |
| `anciennete_locataire`   | Ancienneté du locataire actuel                 |
| `nombre_pieces`          | Nombre de pièces dans le logement              |
| `surface_moyenne`        | Surface moyenne des logements de ce type       |

### Table des Loyers

| Colonne                        | Description                                      |
|--------------------------------|--------------------------------------------------|
| `id_loyer`                     | Identifiant unique pour chaque enregistrement de loyer |
| `id_logement`                  | Référence à `id_logement` dans la table des logements |
| `data_year`                    | Année de collecte des données                    |
| `loyer_1_decile`               | Loyer au 1er décile (10% des loyers les plus bas) |
| `loyer_1_quartile`             | Loyer au 1er quartile (25% des loyers les plus bas) |
| `loyer_median`                 | Loyer médian                                     |
| `loyer_3_quartile`             | Loyer au 3e quartile (75% des loyers les plus bas) |
| `loyer_9_decile`               | Loyer au 9e décile (90% des loyers les plus bas) |
| `loyer_moyen`                  | Loyer moyen                                     |
| `loyer_mensuel_1_decile`       | Loyer mensuel au 1er décile                      |
| `loyer_mensuel_1_quartile`     | Loyer mensuel au 1er quartile                    |
| `loyer_mensuel_median`         | Loyer mensuel médian                             |
| `loyer_mensuel_3_quartile`     | Loyer mensuel au 3e quartile                    |
| `loyer_mensuel_9_decile`       | Loyer mensuel au 9e décile                      |
| `moyenne_loyer_mensuel`        | Moyenne du loyer mensuel                         |
| `nombre_observations`          | Nombre d’observations                           |
| `nombre_logements`             | Nombre de logements                             |

### Table des Observatoires

| Colonne                     | Description                                      |
|-----------------------------|--------------------------------------------------|
| `id_observatoire`           | Identifiant unique pour chaque observatoire     |
| `observatory`               | Nom de l'observatoire                           |
| `zone_complementaire`       | Zone complémentaire (ex. agglomération, ville centre) |
| `methodologie_production`   | Méthodologie de production des données          |

## 2. Création d'une Nouvelle Table de Données

Le code suivant transforme les données du fichier ***CSV*** en tables relationnelles et les exporte en fichiers ***CSV*** séparés.

```python
import pandas as pd

# Lire les données depuis le CSV
df = pd.read_csv('Challenge_2_-_Base_OP_2020_Nationale.csv', delimiter=';')

# Créer la table des logements
logements = df[['Type_habitat', 'epoque_construction_homogene', 'anciennete_locataire_homogene', 'nombre_pieces_homogene', 'surface_moyenne']].drop_duplicates().reset_index(drop=True)
logements.columns = ['type_habitat', 'epoque_construction', 'anciennete_locataire', 'nombre_pieces', 'surface_moyenne']
logements['id_logement'] = logements.index + 1

# Créer la table des loyers
loyers = df[['Data_year', 'loyer_1_decile', 'loyer_1_quartile', 'loyer_median', 'loyer_3_quartile', 'loyer_9_decile', 'loyer_moyen', 'loyer_mensuel_1_decile', 'loyer_mensuel_1_quartile', 'loyer_mensuel_median', 'loyer_mensuel_3_quartile', 'loyer_mensuel_9_decile', 'moyenne_loyer_mensuel', 'nombre_observations', 'nombre_logements', 'Type_habitat']].copy()
loyers = loyers.merge(logements[['type_habitat', 'id_logement']], left_on='Type_habitat', right_on='type_habitat', how='inner')
loyers['id_loyer'] = loyers.index + 1
loyers = loyers[['id_loyer', 'id_logement', 'Data_year', 'loyer_1_decile', 'loyer_1_quartile', 'loyer_median', 'loyer_3_quartile', 'loyer_9_decile', 'loyer_moyen', 'loyer_mensuel_1_decile', 'loyer_mensuel_1_quartile', 'loyer_mensuel_median', 'loyer_mensuel_3_quartile', 'loyer_mensuel_9_decile', 'moyenne_loyer_mensuel', 'nombre_observations', 'nombre_logements']]

# Créer la table des observatoires
observatoires = df[['Observatory', 'Zone_complementaire', 'methodologie_production']].drop_duplicates().reset_index(drop=True)
observatoires.columns = ['observatory', 'zone_complementaire', 'methodologie_production']
observatoires['id_observatoire'] = observatoires.index + 1

# Sauvegarder les nouvelles tables en CSV
logements.to_csv('logements.csv', index=False)
loyers.to_csv('loyers.csv', index=False)
observatoires.to_csv('observatoires.csv', index=False)
```

3. Nettoyage des Données

Voici les étapes pour préparer les données :

- Supprimer les doublons :

  ```python
  df = df.drop_duplicates()
  ```
- Vérifier et traiter les valeurs manquantes :

  ```python

  # Vérifiez les valeurs manquantes
  print(df.isnull().sum())

  # Remplir les valeurs manquantes avec une valeur par défaut ou supprimer les lignes/colonnes
  df = df.fillna({'loyer_moyen': df['loyer_moyen'].median()})
  ```

- Normaliser les formats :

  ```python
  # Convertir les années en entiers
  df['Data_year'] = df['Data_year'].astype(int)

  # Convertir les valeurs monétaires en float
  df['loyer_moyen'] = df['loyer_moyen'].astype(float)
  ```
- Gérer les valeurs extrêmes :

  ```python
  # Détecter les valeurs aberrantes en utilisant les quartiles
  Q1 = df['loyer_moyen'].quantile(0.25)
  Q3 = df['loyer_moyen'].quantile(0.75)
  IQR = Q3 - Q1

  # Filtrer les valeurs aberrantes
  df = df[(df['loyer_moyen'] >= (Q1 - 1.5 * IQR)) & (df['loyer_moyen'] <= (Q3 + 1.5 * IQR))]
  ```

4. Analyse Exploratoire et Visualisations

4.1. Répartition des Loyers

Visualisation des loyers médians par type de logement :

```python
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
sns.boxplot(x='type_habitat', y='loyer_median', data=loyers)
plt.title('Répartition des Loyers Médians par Type de Logement')
plt.xticks(rotation=45)
plt.show()
```
4.2. Évolution des Loyers

Visualisation de l'évolution des loyers médians au fil des années :

```python
plt.figure(figsize=(12, 6))
for log_type in loyers['type_habitat'].unique():
    subset = loyers[loyers['type_habitat'] == log_type]
    plt.plot(subset['Data_year'], subset['loyer_median'], label=log_type)

plt.title('Évolution des Loyers Médians au Fil des Années')
plt.xlabel('Année')
plt.ylabel('Loyer Médian')
plt.legend()
plt.show()
```
4.3. Comparaison des Loyers entre Agglomération et Ville Centre

Comparaison des loyers moyens et des moyennes mensuelles :

```python
plt.figure(figsize=(12, 6))
sns.scatterplot(x='loyer_moyen', y='moyenne_loyer_mensuel', hue='zone_complementaire', data=loyers)
plt.title('Comparaison des Loyers Moyens et Moyennes Mensuelles')
plt.xlabel('Loyer Moyen')
plt.ylabel('Moyenne Loyer Mensuel')
plt.legend(title='Zone Complémentaire')
plt.show()
```
5. Proposition de ***Pipeline de Données*** en ***Temps Réel***

**Ingestion des Données**

***Sources*** : API REST, flux de données en temps réel, fichiers CSV.

***Outils*** :

- `Apache Kafka` : Pour le streaming en temps réel des données.
- `AWS Kinesis` : Pour la collecte et le traitement des flux de données.

**Stockage**

- `Base de Données NoSQL` : Pour stocker les données en temps réel.
- `AWS DynamoDB ou Apache Cassandra` : Adaptés aux écritures rapides et au traitement en temps réel.
- `Data Lake` : Pour le stockage à long terme.
- `AWS S3` ou `Azure Data Lake` : Pour stocker les données brutes et les versions historiques.

**Transformation des Données**

- ETL/ELT :

  - `Apache Flink ou Apache Spark` : Pour le traitement et la transformation des données en temps réel.
  - `AWS Glue` : Pour automatiser les tâches ETL.

**Analyse et Visualisation**

***Outil de BI*** :

- `Power BI` : Pour des dashboards interactifs et des rapports en temps réel.
- `Tableau ou Grafana` : Pour des visualisations et des analyses interactives.

***Dashboards*** :

Créer des visualisations en temps réel qui se mettent à jour automatiquement avec les nouvelles données.

**Monitoring et Maintenance**

***Monitoring*** :

- `Prometheus` : Pour surveiller les métriques du pipeline.
- `Grafana` : Pour visualiser les métriques et les alertes.

***Alertes*** :

- Configurer des alertes pour les erreurs ou les performances du pipeline.

---

**NB** : Le fichier python contenant le code complet est : [process_data.py](./process_data.py)


