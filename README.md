# 🗂️ Texplorateur – Recherche intelligente de fichiers

Texplorateur est une application Windows qui permet d'effectuer une recherche rapide et intuitive dans tous les fichiers d'une extension donnée présents sur votre ordinateur, à la recherche d'une phrase spécifique.

## ✨ Fonctionnalités principales

  + 🔍 Recherche de phrases dans des fichiers .txt, .pdf, .docx et .xlsx

  + 🗃️ Recherche multi-extensions (plusieurs types de fichiers en une seule recherche)

  + 📁 Affichage des chemins complets vers les fichiers trouvés, avec un aperçu du contexte autour de la phrase trouvée

  + 🖱️ Bouton intégré pour ouvrir directement le fichier dans l'explorateur Windows

  + 📊 Barre de progression en temps réel pendant l'analyse, avec possibilité d'annuler une recherche en cours

  + 🕓 Historique des recherches, avec relance en un clic

  + ⚙️ Paramètres personnalisables (thème clair/sombre/système, extensions par défaut)

  + 🧸 Animation mignonne pendant la recherche (plus de fenêtre figée !)

  + 💡 Interface moderne à plusieurs écrans (Accueil, Historique, Paramètres, À propos)

## 🚀 Comment utiliser Texplorateur

  1. Lancez l'application Texplorateur.exe

  2. Depuis l'écran d'accueil, cliquez sur **Nouvelle recherche**

  3. Entrez la phrase à rechercher, choisissez le dossier de départ et les types de fichiers à explorer

  4. Cliquez sur **Rechercher**

  ### Résultats affichés avec :

  - Un aperçu du texte trouvé, en contexte

  - Des boutons pour ouvrir l'emplacement de chaque fichier

  - La possibilité de relancer une recherche précédente depuis l'écran Historique

## 💼 Cas d'usage typiques

  - 📚 Retrouver des documents contenant un passage spécifique

  - 🔎 Vérifier la présence de données sensibles dans des fichiers

  - 🧑‍💼 Utiliser en entreprise pour parcourir des archives textuelles ou des rapports

## 📂 Installation

Si vous avez téléchargé le setup, suivez les étapes :

  - Double-cliquez sur Install_Texplorateur.exe

  - Laissez-vous guider par l'installateur

  - Une fois installé, lancez Texplorateur depuis le menu Démarrer ou le raccourci sur le bureau

## 📋 Configuration minimale requise

  - Windows 10 ou 11

  - Python non requis (fonctionne même sans Python installé)

  - RAM : 2 Go minimum

## 🛠️ Dépendances intégrées

Ce programme a été compilé avec PyInstaller pour inclure :

  - customtkinter (interface graphique)

  - python-docx, PyPDF2, openpyxl (pour lire les différents types de fichiers)

## 🧩 Architecture du projet

Le point d'entrée `Texplorateur_V2.py` lance l'application définie dans le package `texplorateur/` :

```
texplorateur/
  config.py, readers.py, historique.py, son.py, recherche.py, explorateur.py   ← services
  ui/
    theme.py, sidebar.py, confetti.py, cute_animation.py                       ← composants
    screens/  accueil, formulaire, recherche_en_cours, resultats,
              historique, parametres, a_propos                                 ← écrans
    app.py                                                                     ← navigation
```

### 👨‍💻 Auteur : Développé par CONTRACTOR75
