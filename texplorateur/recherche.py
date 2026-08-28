import concurrent.futures
import os
import threading

from .readers import LECTEURS_PAR_EXTENSION, extraire_contexte

# Un pool de threads a un coût fixe (ordonnancement, verrou de progression)
# qui dépasse le gain tant que la lecture de chaque fichier est quasi
# instantanée : mesuré ~20% plus LENT que le séquentiel sur 400 .txt en
# cache disque chaud. Le nombre ou la taille totale des fichiers ne prédit
# pas ce coût — un .txt reste quasi instantané même volumineux, alors que
# .pdf/.docx/.xlsx impliquent un vrai travail de décompression/parsing par
# fichier (mesuré x15 plus rapide en parallèle dès que ce travail domine).
# La décision se base donc sur le TYPE de fichier recherché, pas sur le
# volume.
EXTENSIONS_LOURDES = {".pdf", ".docx", ".xlsx"}
SEUIL_FICHIERS_LOURDS = 6
SEUIL_FICHIERS_LEGERS = 600
NB_THREADS_MAX = 16

# Certains PDF malformés déclenchent des boucles de parsing pathologiques
# dans PyPDF2 (bug connu de la bibliothèque, pas de notre code) — sans
# limite, un seul fichier de ce type peut bloquer toute une recherche
# indéfiniment, sans erreur ni message pour l'utilisateur. On borne donc
# la lecture des formats lourds à ce délai ; au-delà, le fichier est
# ignoré comme s'il n'avait pas pu être lu (cohérent avec le traitement
# des autres erreurs de lecture dans readers.py).
TIMEOUT_LECTURE_LOURDE = 30  # secondes


class MoteurRecherche:
    """Recherche une phrase dans les fichiers d'un dossier, en arrière-plan.

    Le parcours des dossiers reste séquentiel (rapide, ce n'est que de la
    métadonnée). La lecture/analyse du contenu est répartie sur un pool de
    threads uniquement quand le type de fichier recherché le justifie (voir
    EXTENSIONS_LOURDES et les seuils associés) ; sinon elle reste
    séquentielle, plus rapide dans ce cas précis.

    Les callbacks `on_progress` et `on_termine` sont appelés depuis un thread
    de travail (jamais le thread principal, potentiellement plusieurs en
    parallèle pour `on_progress` en mode threads) : à l'appelant de les faire
    retomber sur le thread Tk (typiquement via `root.after(0, ...)`).
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

    def _lister_fichiers(self, dossier, extensions_tuple):
        fichiers = []
        for dossier_courant, _, noms in os.walk(dossier):
            if self._annuler_event.is_set():
                return fichiers, True
            for nom in noms:
                if nom.lower().endswith(extensions_tuple):
                    fichiers.append(os.path.join(dossier_courant, nom))
        return fichiers, False

    @staticmethod
    def _doit_paralleliser(fichiers, extensions):
        a_extension_lourde = any(ext in EXTENSIONS_LOURDES for ext in extensions)
        seuil = SEUIL_FICHIERS_LOURDS if a_extension_lourde else SEUIL_FICHIERS_LEGERS
        return len(fichiers) >= seuil

    @staticmethod
    def _lire_avec_delai_limite(lecteur, chemin, timeout_s):
        """Exécute `lecteur(chemin)` dans un thread démon borné dans le
        temps. Si la lecture n'a pas fini avant `timeout_s`, le fichier est
        abandonné (retourne "") sans attendre la fin réelle du parsing —
        le thread démon continue en arrière-plan mais, étant démon, ne
        bloquera jamais la fermeture de l'application, contrairement à un
        `ThreadPoolExecutor` classique dont les threads ne le sont pas."""
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

        if fichiers and not annulee:
            if self._doit_paralleliser(fichiers, extensions_tuple):
                resultats, annulee = self._analyser_en_parallele(fichiers, phrase)
            else:
                resultats, annulee = self._analyser_sequentiel(fichiers, phrase)
        else:
            resultats = []

        self.on_termine(resultats, len(fichiers), annulee)

    def _analyser_sequentiel(self, fichiers, phrase):
        resultats = []
        for i, chemin in enumerate(fichiers, start=1):
            if self._annuler_event.is_set():
                return resultats, True
            resultat = self._analyser_fichier(chemin, phrase)
            if resultat:
                resultats.append(resultat)
            self.on_progress(i, os.path.dirname(chemin))
        return resultats, False

    def _analyser_en_parallele(self, fichiers, phrase):
        resultats = []
        annulee = False
        verrou = threading.Lock()
        traites = 0

        def travail(chemin):
            nonlocal traites
            resultat = None
            if not self._annuler_event.is_set():
                resultat = self._analyser_fichier(chemin, phrase)
            with verrou:
                traites += 1
                n = traites
            self.on_progress(n, os.path.dirname(chemin))
            return resultat

        nb_threads = min(NB_THREADS_MAX, max(1, len(fichiers)))
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=nb_threads)
        try:
            futures = [executor.submit(travail, chemin) for chemin in fichiers]
            for future in concurrent.futures.as_completed(futures):
                if self._annuler_event.is_set():
                    annulee = True
                    break
                resultat = future.result()
                if resultat:
                    resultats.append(resultat)
        finally:
            # cancel_futures=True : les tâches pas encore démarrées sont
            # abandonnées immédiatement sur annulation, au lieu de toutes
            # s'exécuter avant la fermeture du pool (un shutdown() sans cet
            # argument attend la fin de TOUT le travail déjà soumis, pas
            # seulement des tâches en cours).
            executor.shutdown(wait=True, cancel_futures=True)

        return resultats, annulee
