import json
import os

REPERTOIRE_LOCALES = os.path.join(os.path.dirname(__file__), "locales")
LANGUE_PAR_DEFAUT = "fr"

# (code, nom affiché) — utilisé par l'écran Paramètres pour peupler le
# sélecteur de langue.
LANGUES_DISPONIBLES = [
    ("fr", "Français"),
    ("en", "English"),
]
CODES_LANGUES = [code for code, _ in LANGUES_DISPONIBLES]


class Traducteur:
    """Charge les chaînes traduites depuis `texplorateur/locales/<code>.json`.

    Les clés sont organisées par écran ("parametres.titre") ou regroupées
    sous "commun" pour les libellés partagés (boutons, messages génériques).
    Une clé absente de la langue courante retombe sur le français, puis sur
    la clé elle-même (entre crochets) si elle n'existe nulle part — pour
    repérer facilement une traduction manquante plutôt que de planter.

    Usage prévu (une fois les écrans câblés dessus) :
        app.i18n.t("parametres.titre")
        app.i18n.t("accueil.stats_recherches", n=3)
    """

    def __init__(self, langue=LANGUE_PAR_DEFAUT):
        self._chaines_defaut = self._charger(LANGUE_PAR_DEFAUT)
        self._langue = LANGUE_PAR_DEFAUT
        self._chaines = self._chaines_defaut
        self.definir_langue(langue)

    @property
    def langue(self):
        return self._langue

    def definir_langue(self, code):
        self._langue = code if code in CODES_LANGUES else LANGUE_PAR_DEFAUT
        self._chaines = self._charger(self._langue) if self._langue != LANGUE_PAR_DEFAUT else self._chaines_defaut

    def t(self, cle, **kwargs):
        valeur = self._resoudre(self._chaines, cle)
        if valeur is None:
            valeur = self._resoudre(self._chaines_defaut, cle)
        if valeur is None:
            return f"[{cle}]"
        if not kwargs:
            return valeur
        try:
            return valeur.format(**kwargs)
        except Exception:
            return valeur

    @staticmethod
    def _charger(code):
        chemin = os.path.join(REPERTOIRE_LOCALES, f"{code}.json")
        try:
            with open(chemin, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    @staticmethod
    def _resoudre(chaines, cle):
        courant = chaines
        for partie in cle.split('.'):
            if not isinstance(courant, dict) or partie not in courant:
                return None
            courant = courant[partie]
        return courant
