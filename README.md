<p align="center">
  <img src="image.ico" alt="Logo de Texplorateur" width="96">
</p>

<h1 align="center">Texplorateur</h1>
<p align="center"><strong>Recherche intelligente de phrases dans vos fichiers, sans jamais quitter votre dossier de travail.</strong></p>

<p align="center">
  <img alt="Plateforme" src="https://img.shields.io/badge/plateforme-Windows%2010%2F11-0078D6">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.13-3776AB">
  <img alt="Interface" src="https://img.shields.io/badge/UI-CustomTkinter-2CC985">
  <img alt="Langues" src="https://img.shields.io/badge/langues-FR%20%7C%20EN-informational">
  <img alt="Licence" src="https://img.shields.io/badge/licence-propri%C3%A9taire-lightgrey">
</p>

---

## Sommaire

- [Aperçu](#aperçu)
- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Paramètres](#paramètres)
- [Cas d'usage](#cas-dusage)
- [Lancer depuis les sources](#lancer-depuis-les-sources)
- [Retours et suggestions](#retours-et-suggestions)
- [Licence](#licence)

## Aperçu

Texplorateur est une application de bureau Windows qui recherche une phrase précise à travers tous les fichiers d'un dossier — `.txt`, `.pdf`, `.docx` et `.xlsx` — sans avoir à ouvrir chaque document un par un. L'interface est pensée pour rester réactive même sur de gros volumes de fichiers : le moteur de recherche adapte sa stratégie (séquentielle ou multithread) au type de fichiers ciblé.

## Fonctionnalités

**Recherche**
- Recherche de phrases dans `.txt`, `.pdf`, `.docx` et `.xlsx`, avec sélection multi-extensions en une seule passe
- Barre de progression en temps réel, annulable à tout moment
- Aperçu du contexte autour de chaque occurrence trouvée, et ouverture directe de l'emplacement du fichier dans l'explorateur Windows

**Organisation**
- Historique des recherches, avec relance en un clic ou consultation instantanée des anciens résultats sans relancer l'analyse
- Suppression individuelle des entrées d'historique

**Interface**
- Navigation multi-écrans (Accueil, Historique, Paramètres, À propos) avec barre latérale rétractable
- Thème clair, sombre ou système, avec des contrastes vérifiés pour rester lisibles dans les deux cas
- Interface disponible en français et en anglais
- Confirmation avant de quitter l'application

## Installation

1. Téléchargez le kit d'installation (`Texplorateur_Kit_Install`)
2. Lancez `Install_Texplorateur.exe` et suivez l'installateur
3. Lancez Texplorateur depuis le menu Démarrer ou le raccourci créé sur le bureau

**Configuration minimale** : Windows 10 ou 11, 2 Go de RAM. Aucune installation de Python n'est requise — l'application est autonome.

## Utilisation

1. Depuis l'écran d'accueil, cliquez sur **Nouvelle recherche**
2. Saisissez la phrase recherchée, choisissez le dossier de départ et les types de fichiers à explorer
3. Cliquez sur **Rechercher** — la progression s'affiche en direct, avec possibilité d'annuler
4. Consultez les résultats : aperçu du contexte, bouton pour ouvrir chaque fichier dans l'explorateur

Chaque recherche est conservée dans l'**Historique**, d'où elle peut être relancée ou revue instantanément sans nouvelle analyse.

## Paramètres

L'écran Paramètres permet de personnaliser :

| Réglage | Options |
|---|---|
| Langue de l'interface | Français, English |
| Thème | Clair, Sombre, Système |
| Extensions par défaut | Pré-cochées à l'ouverture du formulaire de recherche |
| Historique | Effacement complet en un clic |

## Cas d'usage

- Retrouver un document contenant un passage précis, sans se souvenir de son nom ni de son emplacement
- Vérifier la présence de données sensibles dans un ensemble de fichiers avant archivage ou partage
- Parcourir des archives textuelles ou des rapports en contexte professionnel

## Lancer depuis les sources

Pour contribuer ou exécuter le projet sans passer par l'installateur :

```bash
git clone <url-du-depot>
cd TextPlorateur
pip install customtkinter pillow python-docx PyPDF2 openpyxl
python Texplorateur_V2.py
```

**Compiler l'exécutable** (nécessite [PyInstaller](https://pyinstaller.org/)) :

```bash
pip install pyinstaller
pyinstaller Texplorateur_V2.spec
```

L'exécutable généré se trouve dans `dist/`.

## Retours et suggestions

Un bug ou une idée d'amélioration ? Un lien de retour est disponible directement dans l'écran **À propos** de l'application une fois celui-ci activé.

## Licence

Logiciel propriétaire fourni « tel quel », sans garantie explicite ou implicite. Vous êtes autorisé à l'installer et l'utiliser librement, ainsi qu'à le partager tel quel et à titre gratuit. Sa modification, sa décompilation et son exploitation commerciale ne sont pas autorisées.
