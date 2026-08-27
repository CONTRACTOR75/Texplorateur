import customtkinter as ctk

from ..config import AppConfig
from ..historique import sauvegarder_historique
from ..i18n import Traducteur
from ..recherche import MoteurRecherche
from ..ressources import chemin_icone
from .modal_confirmation import ModalConfirmation
from .screens.a_propos import AProposScreen
from .screens.accueil import AccueilScreen
from .screens.formulaire import FormulaireScreen
from .screens.historique import HistoriqueScreen
from .screens.parametres import ParametresScreen
from .screens.recherche_en_cours import RechercheEnCoursScreen
from .screens.resultats import ResultatsScreen
from .sidebar import Sidebar

ECRANS_AVEC_SIDEBAR = {"accueil", "historique", "parametres", "a_propos"}


class TexplorateurApp:
    def __init__(self):
        self.config = AppConfig()
        ctk.set_appearance_mode(self.config.theme)
        ctk.set_default_color_theme("blue")

        self.i18n = Traducteur(self.config.langue)

        self.root = ctk.CTk()
        self.root.title("Texplorateur")
        self.root.geometry("980x680")
        self.root.minsize(760, 540)
        self._appliquer_icone()
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        # Le "X" de la fenêtre passe aussi par la confirmation, plutôt que
        # de fermer sans demander alors que le bouton "Quitter" le fait.
        self.root.protocol("WM_DELETE_WINDOW", self.demander_quitter)

        # État de la recherche en cours, mis à jour depuis le thread de
        # recherche : simple mutation de dict, aucun accès Tk depuis ce thread.
        self.etat_progres = {"traites": 0, "dossier_courant": ""}
        self._recherche_courante = None
        self.moteur_recherche = MoteurRecherche(on_progress=self._on_progress, on_termine=self._on_termine)

        self._ecran_actuel = None
        self._construire_layout()
        self.navigate("accueil")

    def _appliquer_icone(self):
        # `.ico` requis par iconbitmap() sous Windows : c'est bien le format
        # de image.ico. Les dialogues (messagebox, etc.) héritent
        # automatiquement de l'icône de leur fenêtre parente, donc ce seul
        # appel couvre toute l'app — il n'y a qu'une fenêtre racine.
        try:
            self.root.iconbitmap(chemin_icone())
        except Exception:
            pass  # Ne bloque pas le lancement si l'icône est introuvable/invalide.

    def _construire_layout(self):
        # Sidebar et contenu restent gridés en permanence : basculer entre
        # écrans "hub" et écrans plein cadre se fait uniquement en changeant
        # l'ordre d'empilement (tkraise/lower), jamais en re-gridant les
        # widgets. Un grid()/grid_remove() répété déclenche un recalcul de
        # géométrie sur toute la fenêtre — visible comme un flash/décalage
        # du contenu à chaque navigation.
        self.sidebar = Sidebar(
            self.root, self, on_navigate=self.navigate, on_nouvelle_recherche=lambda: self.navigate("formulaire"))
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.content = ctk.CTkFrame(self.root, fg_color="transparent")
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        # Conteneur plein cadre, superposé à la sidebar + au contenu, pour
        # les écrans focalisés (formulaire, recherche en cours, résultats).
        self.focus_container = ctk.CTkFrame(self.root, fg_color="transparent", corner_radius=0)
        self.focus_container.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.focus_container.grid_columnconfigure(0, weight=1)
        self.focus_container.grid_rowconfigure(0, weight=1)

        self.screens = {
            "accueil": AccueilScreen(self.content, self),
            "historique": HistoriqueScreen(self.content, self),
            "parametres": ParametresScreen(self.content, self),
            "a_propos": AProposScreen(self.content, self),
            "formulaire": FormulaireScreen(self.focus_container, self),
            "recherche_en_cours": RechercheEnCoursScreen(self.focus_container, self),
            "resultats": ResultatsScreen(self.focus_container, self),
        }
        for screen in self.screens.values():
            screen.grid(row=0, column=0, sticky="nsew")

    def navigate(self, nom, **kwargs):
        if self._ecran_actuel is not None:
            self.screens[self._ecran_actuel].on_hide()

        ecran = self.screens[nom]
        ecran.tkraise()

        if nom in ECRANS_AVEC_SIDEBAR:
            self.sidebar.definir_actif(nom)
            self.sidebar.tkraise()
            self.content.tkraise()
        else:
            self.focus_container.tkraise()

        ecran.on_show(**kwargs)
        self._ecran_actuel = nom

    # -- Recherche --

    def lancer_recherche(self, phrase, extensions, dossier):
        self._recherche_courante = {"phrase": phrase, "extensions": extensions, "dossier": dossier}
        self.etat_progres = {"traites": 0, "dossier_courant": ""}
        self.navigate("recherche_en_cours")
        self.moteur_recherche.lancer(phrase, extensions, dossier)

    def _on_progress(self, traites, dossier_courant):
        self.etat_progres["traites"] = traites
        self.etat_progres["dossier_courant"] = dossier_courant

    def _on_termine(self, resultats, total, annulee):
        self.root.after(0, lambda: self._recherche_terminee(resultats, total, annulee))

    def _recherche_terminee(self, resultats, total, annulee):
        if annulee:
            self.navigate("accueil")
            return

        if self._recherche_courante:
            entree = dict(self._recherche_courante)
            # Les résultats sont sauvegardés avec l'entrée d'historique pour
            # permettre de les reconsulter instantanément (bouton
            # "Résultats"), sans avoir à relancer toute la recherche.
            entree["resultats"] = resultats
            entree["total"] = total
            sauvegarder_historique(entree)

        self.navigate("resultats", resultats=resultats, total=total)

    def afficher_resultats_historique(self, entree):
        resultats = [tuple(r) for r in entree.get("resultats", [])]
        total = entree.get("total", len(resultats))
        self.navigate("resultats", resultats=resultats, total=total, silencieux=True)

    # -- Langue --

    def changer_langue(self, code):
        self.i18n.definir_langue(code)
        self.config.definir_langue(code)

        # Tous les écrans sont retraduits, pas seulement celui affiché : sans
        # ça, un écran masqué garderait ses textes statiques dans l'ancienne
        # langue jusqu'au redémarrage de l'app (son __init__ ne s'exécute
        # qu'une fois). Le contenu dynamique (compteurs, résultats...) se
        # met à jour tout seul au prochain on_show, dans la langue courante.
        self.sidebar.retraduire()
        for screen in self.screens.values():
            screen.retraduire()

    # -- Cycle de vie --

    def demander_quitter(self):
        ModalConfirmation(
            self.root,
            titre=self.i18n.t("quitter.titre"),
            message=self.i18n.t("quitter.message"),
            texte_oui=self.i18n.t("quitter.oui"),
            texte_non=self.i18n.t("quitter.non"),
            on_confirmer=self.root.destroy,
        )

    def run(self):
        self.root.mainloop()
