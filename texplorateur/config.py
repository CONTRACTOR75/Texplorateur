import json
import os

from .i18n import CODES_LANGUES, LANGUE_PAR_DEFAUT

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".texplorateur_config.json")

EXTENSIONS_DISPONIBLES = [".txt", ".pdf", ".docx", ".xlsx"]
THEMES_DISPONIBLES = ["System", "Light", "Dark"]

DEFAUTS = {
    "theme": "System",
    "extensions_par_defaut": [".txt"],
    "langue": LANGUE_PAR_DEFAUT,
}


class AppConfig:
    """Préférences persistées de l'application (thème, extensions par défaut, langue)."""

    def __init__(self):
        self.theme = DEFAUTS["theme"]
        self.extensions_par_defaut = list(DEFAUTS["extensions_par_defaut"])
        self.langue = DEFAUTS["langue"]
        self._charger()

    def _charger(self):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            return

        theme = data.get("theme")
        if theme in THEMES_DISPONIBLES:
            self.theme = theme

        extensions = data.get("extensions_par_defaut")
        if isinstance(extensions, list):
            self.extensions_par_defaut = [e for e in extensions if e in EXTENSIONS_DISPONIBLES]

        langue = data.get("langue")
        if langue in CODES_LANGUES:
            self.langue = langue

    def sauvegarder(self):
        data = {
            "theme": self.theme,
            "extensions_par_defaut": self.extensions_par_defaut,
            "langue": self.langue,
        }
        try:
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def definir_theme(self, theme):
        if theme in THEMES_DISPONIBLES:
            self.theme = theme
            self.sauvegarder()

    def definir_extensions_par_defaut(self, extensions):
        self.extensions_par_defaut = [e for e in extensions if e in EXTENSIONS_DISPONIBLES]
        self.sauvegarder()

    def definir_langue(self, code):
        if code in CODES_LANGUES:
            self.langue = code
            self.sauvegarder()
