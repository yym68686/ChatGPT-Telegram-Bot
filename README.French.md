# ChatGPT Telegram Bot

Rejoignez le chat du [groupe Telegram](https://t.me/+_01cz9tAkUc1YzZl) pour partager votre expérience utilisateur ou signaler des bugs.

## ✨ Fonctionnalités

✅ Support de l'API ChatGPT et GPT4

✅ Prise en charge de la recherche en ligne sur duckduckgo et Google 🔍 . La recherche duckduckgo est fournie par défaut, la recherche Google nécessite une demande API officielle. Il peut répondre aux informations en temps réel que gpt ne pouvait pas répondre auparavant, telles que les tendances populaires sur Weibo aujourd'hui, la météo de certaines zones aujourd'hui, les mises à jour de certaines personnes ou de certaines nouvelles.

✅ Prise en charge des questions-réponses de documents basées sur des bases de données de vecteurs incorporées. Dans la recherche, pour les fichiers PDF trouvés, une recherche sémantique par vecteurs peut être effectuée automatiquement sur le document PDF, et le contenu associé à PDF peut être extrait en fonction de la base de données de vecteurs. Prend en charge l'utilisation de la commande "qa" pour la vectorisation globale d'un site Web contenant un fichier sitemap.xml, et peut répondre aux questions en fonction de la base de données de vecteurs. Convient particulièrement aux sites Web de documentation de projets, aux sites Web de wiki.

✅ Prise en charge de la commutation libre des modèles gpt3.5, gpt4, etc. en utilisant la commande "info" dans la fenêtre de chat

✅ Traitement asynchrone des messages, réponse à plusieurs fils, prise en charge de l'isolation de la conversation, conversation différente pour différents utilisateurs

✅ Prise en charge d'un rendu Markdown de message précis, utilisant mon autre [projet](https://github.com/yym68686/md2tgmd)

✅ Prise en charge de la sortie en continu pour une simulation d'effet de machine à écrire

✅ Prise en charge d'une liste blanche pour éviter les abus et les fuites de renseignements personnels

✅ Plateforme complète, disponible à tout moment et en tout lieu, à tout moment, n'importe où, avec Telegram qui peut briser les barrières de la connaissance

✅ Prise en charge de Zeabur à un bouton, déploiement Replit, coûte zéro, déploiement idiot, support Kuma pour empêcher les interruptions de sommeil. Prend également en charge le déploiement de docker et fly.io

## Variables d'environnement

| Nom de la variable | Remarque |
| ---------------------- | ------------------------------------------------------------ |
| **BOT_TOKEN (obligatoire)**  | Token pour le robot Telegram. Créez un robot sur [BotFather](https://t.me/BotFather) pour obtenir le BOT_TOKEN. |
| **WEB_HOOK (obligatoire)**   | Lorsque le robot Telegram reçoit un message d'un utilisateur, ce message est transmis à WEB_HOOK. Le robot écoutera le WEB_HOOK pour traiter les messages de Telegram reçus dans la boîte. |
| **API (obligatoire)**        | Clé API OpenAI ou tierce partie. |
| API_URL (optionnel)        | Non requis lorsque l'API officielle est utilisée. Si vous utilisez une API tierce, vous devez remplir l'URL du site proxy tiers. La valeur par défaut est : https://api.openai.com/v1/chat/completions |
| GPT_ENGINE (optionnel)     | Modèle de question-réponse par défaut. Défaut : "gpt-3.5-turbo". Cette option peut être librement commutée à l'aide de la commande d'information du robot, et il n'est pas nécessaire de la définir. |
| NICK (optionnel)           | Par défaut vide. Le NICK est le nom du robot. Le robot répond uniquement si un utilisateur commence son message par NICK, sinon il répond à tous les messages. Surtout dans les groupes sans NICK, le robot répondra à tous les messages. |
| PASS_HISTORY (optionnel)   | Par défaut, vrai indique que le robot se souviendra de l'historique de la conversation et tiendra compte du contexte lors de la réponse la prochaine fois. Si pass_history est faux, le robot oublie l'historique de la conversation et ne tient compte que de la conversation actuelle. |
| GOOGLE_API_KEY (optionnel) | Requis pour la recherche sur Google. Si cette variable d'environnement n'est pas définie, la recherche par défaut est fournie par duckduckgo. Créez un identifiant API dans [API et services](https://console.cloud.google.com/apis/api/customsearch.googleapis.com) de Google Cloud. La clé d'API est GOOGLE_API_KEY sur la page de credential. Google permet à une journée de consulter 100 fois, suffisant pour une utilisation légère. Si le quota est atteint, la recherche Google sera automatiquement fermée. |
| GOOGLE_CSE_ID (optionnel)  | Requis pour la recherche sur Google en conjonction avec GOOGLE_API_KEY. Créez un moteur de recherche dans [Programmable Search Engine](https://programmablesearchengine.google.com/). La valeur GOOGLE_CSE_ID est l'identifiant de ce moteur de recherche. |
| whitelist (optionnel)      | Connectez les ID utilisateur autorisés à utiliser le robot. La valeur par défaut est None, c'est-à-dire que le robot est ouvert à tous. |

## Déploiement distant Zeabur (recommandé)

Déploiement en un clic :

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/R5JY5O?referralCode=yym68686)

Pour les mises à jour futures, le déploiement suivant est recommandé :

Commencez par fork le présent dépôt, puis inscrivez-vous sur [Zeabur](https://zeabur.com), l'enveloppe dont la capacité gratuite est suffisante pour une utilisation légère. Importez à partir de votre propre dépôt GitHub et configurez le nom de domaine (qui doit correspondre à WEB_HOOK) et les variables d'environnement, et effectuez un redéploiement. Les mises à jour fonctionnelles ultérieures peuvent être synchronisées avec ce dépôt et redéployées sur Zeabur pour obtenir les dernières fonctionnalités.

## Déploiement à distance Replit

[![Run on Repl.it](https://replit.com/badge/github/yym68686/ChatGPT-Telegram-Bot)](https://replit.com/new/github/yym68686/ChatGPT-Telegram-Bot)

Après avoir importé le dépôt de Github, configurez la commande d'exécution dans "pip install -r requirements.txt > /dev/null && python3 main.py". Dans la colonne de gauche "Tools", sélectionnez "Secrets" et ajoutez les variables d'environnement requises pour le robot. N'oubliez pas d'allumer Always On.

## Déploiement à distance fly.io

Documentation officielle: https://fly.io/docs/

Déployer l'application sur fly.io à l'aide de l'image Docker

```bash
flyctl launch --image yym68686/chatgpt:1.0
```

Saisissez le nom de l'application. Si l'initialisation de Postgresql ou Redis est proposée, refusez.

Déployez selon les instructions. Un nom de domaine de second niveau sera fourni sur le panneau de contrôle du site Web officiel, et le service peut être accédé à l'aide de ce nom de domaine.

Configurer les variables d'environnement

```bash
flyctl secrets set WEB_HOOK=https://flyio-app-name.fly.dev/
flyctl secrets set BOT_TOKEN=bottoken
flyctl secrets set API=
flyctl secrets set COOKIES=
# Facultatif
flyctl secrets set NICK=javis
```

Voir toutes les variables d'environnement

```bash
flyctl secrets list
```

Supprimer une variable d'environnement

```bash
flyctl secrets unset MY_SECRET DATABASE_URL
```

Connexion SSH à un conteneur fly.io

```bash
# Générer une clé
flyctl ssh issue --agent
# Connexion SSH
flyctl ssh establish
```

Vérifiez que l'URL de webhook est correcte

```
https://api.telegram.org/bot<token>/getWebhookInfo
```

## Déploiement Docker

Lancement de conteneur :

```bash
docker run -p 80:8080 -dit \
    -e BOT_TOKEN="telegram bot token" \
    -e WEB_HOOK="https://your_host.com/" \
    -e API="" \
    -e API_URL= \
    yym68686/chatgpt:1.0
```

Si vous préférez Docker Compose, voici un exemple de fichier docker-compose.yml :

```yaml
version: "3.5"
services:
  chatgptbot:
    container_name: chatgptbot
    image: yym68686/chatgpt:1.0
    environment:
      - BOT_TOKEN=
      - WEB_HOOK=
      - API=
      - API_URL=
    ports:
      - 80:8080
```

Lancement du conteneur Docker Compose en arrière-plan

```bash
docker-compose up -d
```

Packager l'image Docker et la pousser sur Docker Hub

```bash
docker build --no-cache -t chatgpt:1.0 -f Dockerfile.build --platform linux/amd64 .
docker tag chatgpt:1.0 yym68686/chatgpt:1.0
docker push yym68686/chatgpt:1.0
```

## Référence

Les projets de référence sont les suivants :

https://core.telegram.org/bots/api

https://github.com/acheong08/ChatGPT

https://github.com/franalgaba/chatgpt-telegram-bot-serverless

https://github.com/gpchelkin/scdlbot/blob/d64d14f6c6d357ba818e80b8a0a9291c2146d6fe/scdlbot/__main__.py#L8

Le rendu markdown des messages utilise mon autre projet : https://github.com/yym68686/md2tgmd

## Historique des Étoiles

<a href="https://github.com/yym68686/ChatGPT-Telegram-Bot/stargazers">
        <img width="500" alt="Star History Chart" src="https://api.star-history.com/svg?repos=yym68686/ChatGPT-Telegram-Bot&type=Date">
</a>