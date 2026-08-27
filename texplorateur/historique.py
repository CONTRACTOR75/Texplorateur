import json
import os

HISTORIQUE_PATH = os.path.join(os.path.expanduser("~"), ".texplorateur_historique.json")
HISTORIQUE_MAX = 15


def charger_historique():
    try:
        with open(HISTORIQUE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def sauvegarder_historique(entree):
    historique = charger_historique()
    historique = [
        h for h in historique
        if not (h["phrase"] == entree["phrase"] and h["dossier"] == entree["dossier"])
    ]
    historique.insert(0, entree)
    historique = historique[:HISTORIQUE_MAX]
    try:
        with open(HISTORIQUE_PATH, 'w', encoding='utf-8') as f:
            json.dump(historique, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    return historique


def supprimer_historique(entree):
    """Retire une entrée précise de l'historique (même critère d'identité
    que la déduplication dans sauvegarder_historique : phrase + dossier)."""
    historique = charger_historique()
    historique = [
        h for h in historique
        if not (h["phrase"] == entree["phrase"] and h["dossier"] == entree["dossier"])
    ]
    try:
        with open(HISTORIQUE_PATH, 'w', encoding='utf-8') as f:
            json.dump(historique, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    return historique


def effacer_historique():
    try:
        with open(HISTORIQUE_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f)
    except Exception:
        pass


def libelle_historique(entree):
    exts = ", ".join(entree["extensions"])
    dossier = entree["dossier"]
    return f'"{entree["phrase"]}" [{exts}] — {os.path.basename(dossier) or dossier}'
