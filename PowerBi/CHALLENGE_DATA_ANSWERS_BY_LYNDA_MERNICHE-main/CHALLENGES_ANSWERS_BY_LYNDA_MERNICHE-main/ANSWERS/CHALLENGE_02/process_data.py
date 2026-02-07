import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import chardet

# Détecter l'encodage du fichier
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(10000))
        return result['encoding']

# Charger les données avec l'encodage détecté
def load_data(file_path):
    encoding = detect_encoding(file_path)
    return pd.read_csv(file_path, delimiter=';', encoding=encoding)

# Nettoyer les données
def clean_data(df):
    df = df.drop_duplicates()
    
    numeric_columns = [
        'loyer_1_decile', 'loyer_1_quartile', 'loyer_median', 'loyer_3_quartile', 
        'loyer_9_decile', 'loyer_moyen', 'loyer_mensuel_1_decile', 'loyer_mensuel_1_quartile',
        'loyer_mensuel_median', 'loyer_mensuel_3_quartile', 'loyer_mensuel_9_decile', 'moyenne_loyer_mensuel'
    ]
    
    for col in numeric_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '.').astype(float)
    
    df['loyer_moyen'] = df['loyer_moyen'].fillna(df['loyer_moyen'].median())
    
    if 'Data_year' in df.columns:
        df['Data_year'] = df['Data_year'].astype(int)
    
    if 'loyer_moyen' in df.columns:
        Q1 = df['loyer_moyen'].quantile(0.25)
        Q3 = df['loyer_moyen'].quantile(0.75)
        IQR = Q3 - Q1
        df = df[(df['loyer_moyen'] >= (Q1 - 1.5 * IQR)) & (df['loyer_moyen'] <= (Q3 + 1.5 * IQR))]
    
    return df

# Créer et sauvegarder les tables
def create_tables(df):

    # Créer la table des Logements
    logements = df[['Type_habitat', 'epoque_construction_homogene', 'anciennete_locataire_homogene', 
                    'nombre_pieces_homogene', 'surface_moyenne']].drop_duplicates().reset_index(drop=True)
    logements.columns = ['type_habitat', 'epoque_construction', 'anciennete_locataire', 'nombre_pieces', 'surface_moyenne']
    logements['id_logement'] = logements.index + 1
    
    # Créer la table des Loyers
    loyers = df[['Data_year', 'loyer_1_decile', 'loyer_1_quartile', 'loyer_median', 'loyer_3_quartile', 
                 'loyer_9_decile', 'loyer_moyen', 'loyer_mensuel_1_decile', 'loyer_mensuel_1_quartile', 
                 'loyer_mensuel_median', 'loyer_mensuel_3_quartile', 'loyer_mensuel_9_decile', 
                 'moyenne_loyer_mensuel', 'nombre_observations', 'nombre_logements', 'Type_habitat']]
    loyers = loyers.merge(logements[['type_habitat', 'id_logement']], left_on='Type_habitat', right_on='type_habitat', how='inner')
    loyers['id_loyer'] = loyers.index + 1
    loyers = loyers[['id_loyer', 'id_logement', 'Data_year', 'loyer_1_decile', 'loyer_1_quartile', 
                     'loyer_median', 'loyer_3_quartile', 'loyer_9_decile', 'loyer_moyen', 
                     'loyer_mensuel_1_decile', 'loyer_mensuel_1_quartile', 'loyer_mensuel_median', 
                     'loyer_mensuel_3_quartile', 'loyer_mensuel_9_decile', 'moyenne_loyer_mensuel', 
                     'nombre_observations', 'nombre_logements']]
    
    # Créer la table des Observatoires
    observatoires = df[['Observatory', 'Zone_complementaire', 'methodologie_production']].drop_duplicates().reset_index(drop=True)
    observatoires.columns = ['observatory', 'zone_complementaire', 'methodologie_production']
    observatoires['id_observatoire'] = observatoires.index + 1
    
    # Sauvegarder les tables en fichiers CSV
    logements.to_csv('logements.csv', index=False)
    loyers.to_csv('loyers.csv', index=False)
    observatoires.to_csv('observatoires.csv', index=False)

# Analyse exploratoire et visualisations
def exploratory_analysis(loyers):

    # Répartition des Loyers Médians par Type de Logement
    plt.figure(figsize=(12, 6))
    if 'type_habitat' in loyers.columns and 'loyer_median' in loyers.columns:
        sns.boxplot(x='type_habitat', y='loyer_median', data=loyers)
        plt.title('Répartition des Loyers Médians par Type de Logement')
        plt.xticks(rotation=45)
        plt.show()

    # Évolution des Loyers Médians au Fil des Années
    plt.figure(figsize=(12, 6))
    if 'type_habitat' in loyers.columns and 'Data_year' in loyers.columns:
        for log_type in loyers['type_habitat'].unique():
            subset = loyers[loyers['type_habitat'] == log_type]
            plt.plot(subset['Data_year'], subset['loyer_median'], label=log_type)
        plt.title('Évolution des Loyers Médians au Fil des Années')
        plt.xlabel('Année')
        plt.ylabel('Loyer Médian')
        plt.legend(title='Type de Logement')
        plt.show()

    # Comparaison des Loyers Moyens et Moyennes Mensuelles
    plt.figure(figsize=(12, 6))
    if 'loyer_moyen' in loyers.columns and 'moyenne_loyer_mensuel' in loyers.columns:
        if 'zone_complementaire' in loyers.columns:
            sns.scatterplot(x='loyer_moyen', y='moyenne_loyer_mensuel', hue='zone_complementaire', data=loyers)
            plt.title('Comparaison des Loyers Moyens et Moyennes Mensuelles')
            plt.xlabel('Loyer Moyen')
            plt.ylabel('Moyenne Loyer Mensuel')
            plt.legend(title='Zone Complémentaire')
            plt.show()

# Documenter le pipeline de données en temps réel
def document_pipeline():

    with open('pipeline_documentation.md', 'w') as f:
        f.write("# Documentation du Pipeline de Données en Temps Réel\n\n")
        f.write("## Objectif\n")
        f.write("Le pipeline de données doit permettre l'ingestion, le stockage, la transformation, l'analyse et la visualisation des données de loyers en temps réel.\n\n")
        f.write("## Ingestion des Données\n")
        f.write("- **Sources** : API REST, flux de données en temps réel, fichiers CSV.\n")
        f.write("- **Outils** :\n")
        f.write("  - **Apache Kafka** : Pour le streaming en temps réel des données.\n")
        f.write("  - **AWS Kinesis** : Pour la collecte et le traitement des flux de données.\n\n")
        f.write("## Stockage\n")
        f.write("- **Base de Données NoSQL** : Pour stocker les données en temps réel.\n")
        f.write("  - **AWS DynamoDB** ou **Apache Cassandra** : Adaptés aux écritures rapides et au traitement en temps réel.\n")
        f.write("- **Data Lake** : Pour le stockage à long terme.\n")
        f.write("  - **AWS S3** ou **Azure Data Lake** : Pour stocker les données brutes et les versions historiques.\n\n")
        f.write("## Transformation des Données\n")
        f.write("- **ETL/ELT** :\n")
        f.write("  - **Apache Flink** ou **Apache Spark** : Pour le traitement et la transformation des données en temps réel.\n")
        f.write("  - **AWS Glue** : Pour automatiser les tâches ETL.\n\n")
        f.write("## Analyse et Visualisation\n")
        f.write("- **Outil de BI** :\n")
        f.write("  - **Power BI** : Pour des dashboards interactifs et des rapports en temps réel.\n")
        f.write("  - **Tableau** ou **Grafana** : Pour des visualisations et des analyses interactives.\n")
        f.write("- **Dashboards** :\n")
        f.write("  - Créez des visualisations en temps réel qui se mettent à jour automatiquement avec les nouvelles données.\n\n")
        f.write("## Monitoring et Maintenance\n")
        f.write("- **Monitoring** :\n")
        f.write("  - **Prometheus** : Pour surveiller les métriques du pipeline.\n")
        f.write("  - **Grafana** : Pour visualiser les métriques et les alertes.\n")
        f.write("- **Alertes** :\n")
        f.write("  - Configurez des alertes pour les erreurs ou les performances du pipeline.\n")

def main(file_path):

    df = load_data(file_path)
    df_cleaned = clean_data(df)
    create_tables(df_cleaned)
    
    loyers = df_cleaned[['Data_year', 'loyer_median', 'loyer_moyen', 'moyenne_loyer_mensuel', 'Type_habitat', 'Zone_complementaire']].dropna()
    loyers.columns = ['Data_year', 'loyer_median', 'loyer_moyen', 'moyenne_loyer_mensuel', 'type_habitat', 'zone_complementaire']
    exploratory_analysis(loyers)

    document_pipeline()

# Exemple d'utilisation
if __name__ == "__main__":
    
    file_path = 'Challenge_2_-_Base_OP_2020_Nationale.csv'
    main(file_path)
