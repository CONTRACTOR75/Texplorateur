import os
import threading

from .readers import LECTEURS_PAR_EXTENSION, extraire_contexte


class MoteurRecherche:
    """Recherche une phrase dans les fichiers d'un dossier, en arrière-plan.

    Les callbacks `on_progress` et `on_termine` sont appelés depuis le thread
    de recherche : à l'appelant de les faire retomber sur le thread Tk
    (typiquement via `root.after(0, ...)`).
    """

    def __init__(self, on_progress, on_termine):
        self.on_progress = on_progress  # (fichiers_traites, dossier_courant) -> None
        self.on_termine = on_termine  # (resultats, total_fichiers, annulee) -> None
        self._annuler_event = threading.Event()

    def lancer(self, phrase, extensions, dossier):
        self._annuler_event.clear()
        threading.Thread(target=self._tache, args=(phrase, extensions, dossier), daemon=True).start()

    def annuler(self):
        self._annuler_event.set()

    def _tache(self, phrase, extensions, dossier):
        extensions_tuple = tuple(extensions)
        resultats = []
        total_fichiers = 0
        annulee = False

        for dossier_courant, _, fichiers in os.walk(dossier):
            if self._annuler_event.is_set():
                annulee = True
                break

            for fichier in fichiers:
                if self._annuler_event.is_set():
                    annulee = True
                    break

                if not fichier.lower().endswith(extensions_tuple):
                    continue

                chemin = os.path.join(dossier_courant, fichier)
                total_fichiers += 1

                ext = os.path.splitext(chemin)[1].lower()
                lecteur = LECTEURS_PAR_EXTENSION.get(ext)
                contenu = lecteur(chemin) if lecteur else ""

                if phrase.lower() in contenu.lower():
                    contexte = extraire_contexte(contenu, phrase)
                    resultats.append((os.path.basename(chemin), chemin, contexte))

                self.on_progress(total_fichiers, dossier_courant)

            if annulee:
                break

        self.on_termine(resultats, total_fichiers, annulee)
