# App-Sup-Trading

## Introduction

Le projet App-Sup-Trading est une initiative visant à développer une solution d'automatisation, appelée Robotic Process Automation (RPA), pour la collecte régulière des cours de certaines actions du CAC 40. L'objectif principal est de construire une base de données robuste pour l'entraînement d'un algorithme de trading haute fréquence. Ce projet a pour but l'acquisition des données en temps réel du marché boursier des CAC40. Notre solution intègre un robot conçu pour récupérer les cours d'action depuis le site de Boursorama en utilisant le scraping en Python.

## Robot d'Extraction de Données de Marché Financier

### Introduction

Ce document technique détaille le fonctionnement d'un robot automatisé conçu pour extraire et stocker les données financières en temps réel des marchés boursiers, en particulier celles liées au CAC40, grâce à l'utilisation de la bibliothèque Beautiful Soup. Le script Python développé pour cette tâche interagit avec une base de données PostgreSQL pour gérer les données recueillies. Ce processus inclut la création de tables de base de données, l'insertion des données en temps réel, et le suivi des opérations via des fichiers de log.

### Structure du Robot

Le robot est constitué de plusieurs modules clés, chacun dédié à une tâche spécifique :

- **Modules.ConfiParser** : Ce module inclut une fonction nécessaire pour récupérer les paramètres du programme à partir du ficher de configuration.
- **Modules.DatabaseFunctions** : Ce module inclut des fonctions nécessaires pour récupérerétablir une connexion avec la base de données PostgreSQL, créer les tables et pour l'insertion des données.
- **Modules.DateTime** : Contient la fonction qui gère les temps d'attente.
- **Modules.Scraping** : Contient les fonctions de scraping des données boursières, une fonction pour le site de CAC40 et une autre pour les 40 sites web des entreprises.
- **Modules.SendMail** : Gère l'envoi d'emails avec les fichiers de données extraits.

## Flux de Travail du Robot

Le robot suit un processus structuré pour extraire, stocker et gérer les données financières en temps réel. Chaque étape du processus est conçue pour fonctionner de manière autonome et efficace :

1. **Connexion à la Base de Données** :
   - Initie la connexion à PostgreSQL en utilisant les paramètres définis dans `./Config/Config.ini`.
   - Cette connexion permet au robot d'interagir directement avec la base de données pour toutes les opérations nécessaires.

2. **Création des Tables** :
   - Vérifie l'existence et crée, si nécessaire, deux tables principales : `cac40` et `companies`.

3. **Extraction des Données** :
   - Le programme se lance dans une boucle infinie, et doit être hébergé sur un serveur et pas sur une machine simple, après avoir vérifié l'heure et la journée (si jour ouvré), le programme interroge les sites Boursorama avec leuurs Urls qui sont dans le fichier de configuration afin de vérifier leurs accessibilités. Ainsi, il récupère les codes HTML avec lesquels on récupère toutes les données des actions à l'aide des balises des classes et divisions.

4. **Insertion des Données dans la Table Daily** :
   - Insère les nouvelles données récupérées dans la table `cac40_daily_data` après chaque récupération de données entre 9h et 18:05 tous les jours ouvrés puisque les marchés sur les site de Boursorama sont ouverts sur cette plage horaire.

5. **Exportation des Données et Envoi par Email** :
   - À 18:06, On sort de la marge horaire, et on recupère les données de la clôture pour les envoyer par mail à l'administrateur sous format CSV.
   - Envoie ce fichier par email à une liste de destinataires prédéfinie dans le fichier de configuration, facilitant la diffusion rapide des informations.
   - Une fois le fichier envoyé, il sera supprimé puisque toutes les données sont dèjà dans la base de données.

6. **Robot en attente de la réouverture des marchés** :
   - Une fois le mail envoyé, le programme attendra jusqu'au prochain jour ouvré à 9h pour relancer les récupération des nouvelles données et ça à l'aide des fonctions WaitUntil et Sleep qui vont rendormir tous les processus.

Ce flux de travail garantit une collecte et une gestion efficaces des données de marché, soutenant l'analyse et le trading en fournissant des données actualisées et archivées de manière fiable et accessible.

### Configuration et Dépendances

- **PostgreSQL** et **Python 3.x** comme base technologique.
- **Bibliothèques Python** nécessaires : `beautifulsoup4`, `bs4`, `psycopg2`, `requests`, ainsi que `datetime` et `time` pour la gestion temporelle.
- **Configuration JSON** : Contient les paramètres de connexion à la base de données et la configuration du mail.

### Gestion des Logs

L'application utilise le module `logging` pour enregistrer les événements clés, facilitant ainsi le débogage et le suivi efficace de son utilisation.
- Les erreurs dans le fichier ./Logs/ERROR_<DATE>.log
- Les informations dans le fichier ./Logs/INFO_<DATE>.log



# Guide de Configuration Technique pour App-Sup-Trading

Ce guide détaille les étapes nécessaires au déploiement de la solution App-Sup-Trading, y compris la préparation de l'environnement, l'installation des dépendances, et le lancement de l'application.

## Prérequis

- Python 3.x installé sur votre machine.
- Accès à un serveur PostgreSQL.
- Hébergement sur une VM sur un serveur physique ou sur le Cloud.


## Étapes de Configuration

### 1. Récupération du Projet

Clonez ou téléchargez le dossier du projet depuis son dépôt Git vers un répertoire de votre choix :

```bash
git clone https://github.com/amayasmh/Sup-Trading.git
```

### 2. Création et activation d'un Environnement Virtuel

Dans le dossier du projet, créez un environnement virtuel nommé `env` :

```bash
python -m venv env
```

Activez cet environnement virtuel :

- Sous Windows :

  ```cmd
  .\env\Scripts\activate
  ```

- Sous macOS et Linux :

  ```bash
  source env/bin/activate
  ```

### 3. Installation des Dépendances

Avec l'environnement activé, installez les dépendances nécessaires via :

```bash
pip install -r requirements.txt
```

Assurez-vous que `requirements.txt` est présent à la racine du projet.

### 4. Préparation des Dossiers

- **Dossier Logs** : Vérifier l'existence sinon créez un dossier `Logs` à la racine pour les fichiers générés :

  ```bash
  mkdir Logs
  ```

- **Dossier Data** : Créez un dossier `Data` pour les fichiers de données :

  ```bash
  mkdir Data
  ```

### 5. Configuration de la Base de Données et de l'Email

#### Base de Données

Modifiez le fichier de configuration (typiquement `Config.ini` dans le dossier `Config`) avec les paramètres de votre base de données PostgreSQL :

```[Postgresql]
host = nom_de_hôte
user = nom_de_l_utilisateur
password = mot_de_passe
dbname = nom_de_la_base_de_donnees
port = numero_de_port(par défaut 5432)
```

#### Email

Dans le même dossier `Config`, modifiez le fichier pour la configuration de l'email (`MailConfig.json`) avec les paramètres suivants pour configurer le serveur SMTP et les destinataires des emails :

```[Mailing]
host = nom_de_hôte
port = numero_de_port(465 pour SMTP)
user = adresse_mail_envoi
password = code_application_de_messagerie (regardez cette video pour savoir d'ou le récupérer https://m.youtube.com/watch?v=46-SyQlxlCQ&pp=ygUUZW52b3llciBtYWlsIHB5dGhvbiA%3D )
to = email_de_destinataires (séparés pas une virgule si plusieurs)
```
### 6. Déploiement et Automatisation du robot

Le robot d'extraction de données doit être déployé et exécuté sur un serveur qui sera en marche 24/7 pour assurer son exécution pendant les heures de marché et suivre les cours en temps réél.
Votre robot est maintenant configuré pour s'exécuter automatiquement pendant les heures de marché sur Linux et Windows. Assurez-vous de tester la tâche planifiée pour vérifier qu'elle démarre comme prévu.
Une fois le programme est lancé sur le serveur, il s'en chargera de gérer les temps d'exécution (d'ouverture et de clôture des marchés)

### 7. Lancement de programme 

Pour lancer le programme, il suffit de lancer le fichier exec.bat après avoir installer les bibliothèques nécessaires, le exec.bat compilera le programme à l'aide de l'interpréteur Python de l'environnement virtuel du dossier env.
Une fenêtre du terminal s'ouvrira sur laquelle les messages d'informations des grandes étapes vont s'afficher.

### 8. Visualisation
Le fichier SupTrading.pbix est un fichier Power BI, afin de visualiser le suivi des actions, vous devez avoir l'outil installé, des tableaux de reporting sont en place, il faut juste refaire la connexion avec la base de données une fois le programme est lancé et les tables ont été créées.

## Conclusion

Suivez ce guide pour configurer et démarrer la solution App-Sup-Trading sur votre système. Cette configuration de base vous permettra de lancer l'application et d'accéder à ses fonctionnalités.
