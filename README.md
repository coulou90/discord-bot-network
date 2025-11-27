🤖 NetworkBot — Projet Discord Bot (B2 Cybersécurité)

NetworkBot est un bot Discord développé dans le cadre du Projet de Rattrapage B2.  
Il intègre plusieurs fonctionnalités avancées imposées dans le sujet :

- Structures de données (liste chaînée, arbre binaire)
- Système conversationnel basé sur un arbre décisionnel
- Historique persistant des commandes
- Sauvegarde JSON
- Bonus : Quiz réseau + XP & niveaux
- Bonus : Statistiques administrateur
- Bonus : Commandes avancées et structure logique propre

📌 Sommaire

1. Fonctionnalités Principales
2. Fonctionnalités Bonus
3. Architecture du Projet
4. Structures de Données Implémentées
5. Installation et Lancement
6. Commandes du Bot
7. Sauvegarde Persistante
8. Auteur

🚀 Fonctionnalités Principales

1. Historique des Commandes (Liste Chaînée)

Chaque utilisateur possède un historique personnel :

- !last → Dernière commande
- !history → Historique complet
- !clear_history → Vider l’historique

L’historique utilise une liste chaînée implémentée à la main, comme exigé.

2. Système de Discussion (Arbre Binaire)

Avec la commande :

!start

Le bot déclenche une conversation guidée par un arbre binaire.

L'utilisateur répond par 1 ou 2 selon les choix proposés.

Commandes supplémentaires :

- !reset → Revenir à la racine de l’arbre  
- !speak_about <mot> → Vérifie si un thème existe dans l’arbre  
- Résultat final selon le chemin suivi

Les noeuds sont codés manuellement.


3. Sauvegarde Persistante (JSON)

Toutes les données sont enregistrées automatiquement à l'arrêt du bot :

- Historique des commandes
- Position dans l’arbre
- XP / niveaux
- Progrès dans le quiz

Fichier sauvegardé :

/data/save.json

Et rechargé au démarrage.

⭐ Fonctionnalités Bonus

4. Système d’XP + Niveaux

Chaque commande donne de l’XP.  
Les utilisateurs montent de niveau automatiquement.

!level
!rank
Affiche le niveau et le classement des utilisateurs.
Bonus d'XP à la fin du quiz.

5. Quiz Réseau Interactif

!quiz

Le bot pose des questions sur les réseaux.  

- 5 questions
- Réponses : 1 / 2 / 3
- Score final + bonus XP
- 100% intégré au système XP

6. Statistiques Administrateur

!stats

Affiche des statistiques globales :

Affiche un embed professionnel :

- Nombre total d’utilisateurs
- Commandes utilisées
- XP global
- Uptime du bot
- Utilisateurs en quiz / discussion
- Etat de la sauvegarde

📂 Architecture du Projet

discord-bot-network/
│
├── bot.py # Code principal
├── config.py # Token (non versionné)
├── history.py # Liste chaînée pour historique
├── dialogue_tree.py # Arbre binaire de discussion
├── storage.py # Sauvegarde / chargement JSON
│
└── data/
└── save.json # Sauvegarde persistante


🧩 Structures de Données Implémentées

Liste chaînée  
Utilisée pour gérer l'historique utilisateur.

Arbre binaire  
Utilisé pour la discussion guidée.

                                        ┌──────────────────────────────────────┐
                                        │                ROOT                  │
                                        │ Tu préfères travailler surtout avec :│
                                        │   1️⃣ Cisco      |   2️⃣ Linux        │
                                        └──────────────────────────────────────┘
                                             /                                     \
                                            /                                       \
                                           /                                         \

      ┌──────────────────────────────────────────────┐             ┌───────────────────────────────────────────┐
      │                    Q2 CISCO                  │             │                   Q2 LINUX                │
      │ Avec Cisco, tu préfères :                   │             │ Sur Linux, tu préfères travailler sur :    │
      │ 1️⃣ Config réseau | 2️⃣ Dépannage réseau       │             │ 1️⃣ Administration   |  2️⃣ Automatisation  │
      └──────────────────────────────────────────────┘             └───────────────────────────────────────────┘
                   /                      \                                   /                    \
                  /                        \                                 /                      \

 ┌──────────────────────────────┐   ┌──────────────────────────────┐   ┌────────────────────────────┐   ┌─────────────────────────────┐
 │        Q3 CISCO CONFIG       │   │     Q3 CISCO DÉPANNAGE       │   │     Q3 LINUX SERVICES       │   │       Q3 LINUX AUTO         │
 │ Tu préfères travailler sur:  │   │ En dépannage, tu te vois :   │   │ Tu préfères gérer :         │   │ Tu veux automatiser :        │
 │1️⃣ LAN/VLAN | 2️⃣ Sécurité    │   │ 1️⃣ Analyse    | 2️⃣ NOC      │   │ 1️⃣ Services | 2️⃣ Virtualisation │ │ 1️⃣ Déploiements | 2️⃣ Supervision │
 └──────────────────────────────┘   └──────────────────────────────┘   └────────────────────────────┘   └─────────────────────────────┘
       /              \                   /             \                   /           \                     /                 \
      /                \                 /               \                 /             \                   /                   \

 ┌────────────────────┐ ┌────────────────────────┐ ┌────────────────────────┐ ┌──────────────────────────┐ ┌───────────────────────┐ ┌───────────────────────┐
 │   LEAF CISCO LAN   │ │   LEAF CISCO SECURITY  │ │  LEAF SUPPORT N2      │ │     LEAF NOC             │ │   LEAF LINUX ADMIN    │ │ LEAF VIRTUALISATION   │
 │ Admin LAN / VLAN   │ │ Admin Sécurité réseau  │ │ Tech support N2       │ │ Ingénieur NOC            │ │ Admin systèmes Linux  │ │ Ingénieur VM / LXC    │
 └────────────────────┘ └────────────────────────┘ └────────────────────────┘ └──────────────────────────┘ └───────────────────────┘ └───────────────────────┘

                       ┌──────────────────────────┐       ┌──────────────────────────┐
                       │      LEAF DEVOPS         │       │   LEAF MONITORING        │
                       │ Automatisation réseau    │       │ Ingénieur Monitoring     │
                       └──────────────────────────┘       └──────────────────────────┘


Dictionnaires structurés  
Pour XP, quiz, positions, etc.

Système de sauvegarde custom  
Sans base de données, juste JSON.


⚙ Installation et Lancement

1️⃣ Cloner le projet

git clone https://github.com/coulou90/discord-bot-network


2️⃣ Installer les dépendances

pip install discord.py

3️⃣ Configurer le token

Créer un fichier config.py avec :

TOKEN = "VOTRE_TOKEN_ICI"

4️⃣ Lancer le bot

python bot.py

📝 Commandes du Bot

Commande	                   Description
!ping	                          Test
!start	                   Démarre la discussion
!reset	                   Réinitialise l’arbre
!speak_about X	            Cherche un thème
!history	                 Historique
!last	                     Dernière commande
!clear_history	              Efface l’historique
!quiz	                           Quiz réseau
!level	                         Voir son niveau
!rank	                           Classement
!stats	                          Statistiques admin

💾 Sauvegarde Persistante

Toutes les données sont sauvegardées dans /data/save.json à l'arrêt du bot et rechargées au démarrage.

La sauvegarde est gérée automatiquement grâce à atexit :

Pas de perte de données

Reprise automatique de session

Gestion d’un fichier JSON formaté


👤 Auteur
Souleymane Coulibaly
Bachelor2 Cybersécurité – Paris Ynov Campus 2025
