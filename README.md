# CineBot

CineBot est un bot Discord qui permet d'obtenir des informations sur les films, séries et personnalités du monde cinématographique grâce à l'API TMDB.

## 📋 Description

CineBot vous permet de rechercher et d'afficher :

- Des informations sur les films (synopsis, date de sortie, note, etc.)
- Des informations sur les séries TV
- Des détails sur les acteurs, réalisateurs et autres personnes du monde du cinéma

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- Un compte Discord Developer pour créer un bot
- Une clé API TMDB

### Étapes d'installation

1. Clonez le dépôt :

    ```bash
    git clone https://github.com/votre_utilisateur/CineBot.git
    cd CineBot
    ```

2. Installation des dépendances :

    ```bash
    pip install -r requirements.txt
    ```

3. Créez un fichier `.env` à la racine du projet avec les variables suivantes :

    ```env
    DISCORD_TOKEN=votre_token_discord
    TMDB_API_KEY=votre_cle_api_tmdb
    ```

## 💻 Utilisation

1. Lancez le bot :

    ```bash
    python main.py
    ```

2. Dans Discord, utilisez les commandes suivantes :

    - `/search_movie [titre]` - Rechercher un film
    - `/search_tv [titre]` - Rechercher une série
    - `/search_person [nom]` - Rechercher une personnalité

## 🧰 Structure du projet

- `main.py` - Point d'entrée principal du bot Discord
- `cinebot.py` - Contient les classes qui interagissent avec l'API TMDB
- `objs` - Modèles de données pour films, séries et personnes
- `cogs` - Extensions modulaires pour les commandes Discord

## 📝 À faire

- [ ] Optimiser le code
- [ ] Ajouter des informations sur les plateformes de streaming
- [ ] Améliorer l'interface utilisateur dans Discord
- [ ] Ajouter des commandes supplémentaires

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à proposer une pull request.

## 📄 Licence

MIT
