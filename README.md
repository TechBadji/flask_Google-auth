Description orientée fonction et usage (Idéale pour les contributeurs)
Application web minimale pour la gestion des utilisateurs, développée avec Python et Flask.
Ce dépôt sert de modèle pour mettre en place un système de connexion polyvalent. Il gère deux types d'utilisateurs en parallèle :
  1. Les utilisateurs inscrits localement.
  2. Les utilisateurs se connectant via des fournisseurs externes (Google OAuth/OIDC).
Technologies Clés : Flask, Authlib, Flask-SQLAlchemy, et une gestion sécurisée des secrets d'API via les variables d'environnement.
Le code inclut des mécanismes robustes pour gérer les sessions et les jetons ID (nonce, access_token).
