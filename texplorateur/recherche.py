import os
import threading

from .readers import LECTEURS_PAR_EXTENSION, extraire_contexte

EXTENSIONS_LOURDES = {".pdf", ".docx", ".xlsx"}

# Certains PDF malformés déclenchent des boucles de parsing pathologiques
# dans PyPDF2 (bug connu de la bibliothèque, pas de notre code) — sans
# limite, un seul fichier de ce type peut bloquer toute une recherche
# indéfiniment, sans erreur ni message pour l'utilisateur. On borne donc
# la lecture des formats lourds à ce délai ; au-delà, le fichier est
# ignoré comme s'il n'avait pas pu être lu (cohérent avec le traitement
# des autres erreurs de lecture dans readers.py).
TIMEOUT_LECTURE_LOURDE = 30  # secondes

# os.path.isjunction n'existe qu'à partir de Python 3.12 : repli silencieux
# (aucun élagage) sur un interpréteur plus ancien plutôt qu'un crash.
_est_jonction = getattr(os.path, "isjunction", lambda chemin: False)


class MoteurRecherche:
    """Recherche une phrase dans les fichiers d'un dossier, en arrière-plan
    (un seul thread dédié, séquentiel).

    Le traitement multithread a été essayé puis retiré : mesuré avec du
    vrai parsing PyPDF2 (pas un `time.sleep()` en guise de simulation, qui
    libère le GIL et ne représente pas un travail CPU réel), paralléliser
    n'apporte aucun gain net (x0.96 à x0.98, parfois plus lent que
    séquentiel) car PyPDF2/python-docx/openpyxl sont du pur Python qui
    retient le GIL — et ça a un coût bien réel : jusqu'à x2 de
    ralentissement du thread principal Tk avec 16 threads simultanés sur du
    PDF normal, et une contention bien plus sévère sur des fichiers
    pathologiques (mesuré jusqu'à x66 dans un scénario extrême), ce qui
    explique les gels d'interface observés. Avec le seul thread de
    recherche déjà nécessaire (aucune parallélisation), la contention
    mesurée tombe à x1.13 — négligeable.

    Les callbacks `on_progress` et `on_termine` sont appelés depuis le
    thread de recherche (jamais le thread principal) : à l'appelant de les
    faire retomber sur le thread Tk (typiquement via `root.after(0, ...)`).
    """

    def __init__(self, on_progress, on_termine):
        self.on_progress = on_progress  # (fichiers_traites, dossier_courant, phase) -> None
        self.on_termine = on_termine  # (resultats, total_fichiers, annulee) -> None
        self._annuler_event = threading.Event()

    def lancer(self, phrase, extensions, dossier):
        self._annuler_event.clear()
        threading.Thread(target=self._tache, args=(phrase, extensions, dossier), daemon=True).start()

    def annuler(self):
        self._annuler_event.set()

    def _lister_fichiers(self, dossier, extensions_tuple):
        fichiers = []
        for dossier_courant, sous_dossiers, noms in os.walk(dossier):
            if self._annuler_event.is_set():
                return fichiers, True

            # Une jonction NTFS (ex: AppData\Local\Application Data, souvent
            # auto-référentielle) n'est pas détectée par os.path.islink() et
            # serait donc parcourue comme un dossier normal par os.walk, avec
            # un vrai risque de boucle ou de profondeur démesurée sur un
            # dossier de départ large (C:\, profil utilisateur...). On
            # l'exclut de la descente en modifiant `sous_dossiers` en place
            # (mécanisme standard d'élagage d'os.walk).
            sous_dossiers[:] = [
                d for d in sous_dossiers
                if not _est_jonction(os.path.join(dossier_courant, d))
            ]

            for nom in noms:
                if nom.lower().endswith(extensions_tuple):
                    fichiers.append(os.path.join(dossier_courant, nom))

            # Sur un dossier de départ large, le seul parcours (avant même
            # de lire un fichier) peut prendre longtemps : sans ce signal,
            # l'écran "Recherche en cours" resterait figé sur "Parcours des
            # dossiers…" sans aucune preuve que l'app travaille toujours.
            self.on_progress(len(fichiers), dossier_courant, "parcours")

        return fichiers, False

    @staticmethod
    def _lire_avec_delai_limite(lecteur, chemin, timeout_s):
        """Exécute `lecteur(chemin)` dans un thread démon borné dans le
        temps. Si la lecture n'a pas fini avant `timeout_s`, le fichier est
        abandonné (retourne "") sans attendre la fin réelle du parsing —
        le thread démon continue en arrière-plan mais, étant démon, ne
        bloquera jamais la fermeture de l'application."""
        resultat = {}

        def cible():
            try:
                resultat["valeur"] = lecteur(chemin)
            except Exception:
                resultat["valeur"] = ""

        thread = threading.Thread(target=cible, daemon=True)
        thread.start()
        thread.join(timeout_s)
        return resultat.get("valeur", "")

    @classmethod
    def _analyser_fichier(cls, chemin, phrase):
        ext = os.path.splitext(chemin)[1].lower()
        lecteur = LECTEURS_PAR_EXTENSION.get(ext)
        if lecteur is None:
            return None

        if ext in EXTENSIONS_LOURDES:
            contenu = cls._lire_avec_delai_limite(lecteur, chemin, TIMEOUT_LECTURE_LOURDE)
        else:
            contenu = lecteur(chemin)

        if contenu and phrase.lower() in contenu.lower():
            return (os.path.basename(chemin), chemin, extraire_contexte(contenu, phrase))
        return None

    def _tache(self, phrase, extensions, dossier):
        extensions_tuple = tuple(extensions)
        fichiers, annulee = self._lister_fichiers(dossier, extensions_tuple)

        resultats = []
        if fichiers and not annulee:
            for i, chemin in enumerate(fichiers, start=1):
                if self._annuler_event.is_set():
                    annulee = True
                    break
                resultat = self._analyser_fichier(chemin, phrase)
                if resultat:
                    resultats.append(resultat)
                self.on_progress(i, os.path.dirname(chemin), "analyse")

        self.on_termine(resultats, len(fichiers), annulee)
