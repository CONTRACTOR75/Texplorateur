import customtkinter as ctk

from ...readers import tronquer_chemin
from ..cute_animation import CuteAnimation
from ..theme import ACCENT_GRIS, font_sous_titre
from .base import Screen


class RechercheEnCoursScreen(Screen):
    """Écran plein cadre affiché pendant une recherche : rien d'autre à l'écran."""

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._actif = False

        # Carte bordée (même traitement que l'écran Formulaire) plutôt que du
        # contenu flottant directement sur le fond : sur une fenêtre large
        # ou maximisée, un petit bloc de texte centré sans ancrage visuel
        # se perd dans le vide et donne une impression de mise en page
        # déséquilibrée.
        carte = ctk.CTkFrame(self, corner_radius=14)
        carte.place(relx=0.5, rely=0.46, anchor="center")
        centre = ctk.CTkFrame(carte, fg_color="transparent")
        centre.pack(padx=56, pady=48)

        self.cute_animation = CuteAnimation(centre, app)
        self.cute_animation.pack()

        self.barre = ctk.CTkProgressBar(centre, mode="indeterminate", width=280)
        self.barre.pack(pady=(20, 8))

        self.label_compteur = ctk.CTkLabel(centre, text="", font=font_sous_titre(11), text_color=ACCENT_GRIS)
        self.label_compteur.pack()

        self.bouton_annuler = ctk.CTkButton(
            centre, text=self.t("commun.annuler"), fg_color="transparent", border_width=1,
            text_color=("gray10", "gray90"), command=self._annuler,
        )
        self.bouton_annuler.pack(pady=(24, 0))

    def retraduire(self):
        # Écran non actif au moment d'un changement de langue (celui-ci se
        # fait depuis Paramètres) : seul le libellé "Annuler" par défaut a
        # besoin d'être resynchronisé, "Annulation…" ne peut pas être affiché
        # ici puisqu'aucune recherche n'est en cours pendant ce changement.
        self.bouton_annuler.configure(text=self.t("commun.annuler"))

    def on_show(self, **kwargs):
        self._actif = True
        self.bouton_annuler.configure(state="normal", text=self.t("commun.annuler"))
        self.label_compteur.configure(text=self.t("recherche_en_cours.parcours_dossiers"))
        self.cute_animation.start()
        self.barre.start()
        self._rafraichir()

    def on_hide(self):
        self._actif = False
        self.cute_animation.stop()
        self.barre.stop()

    def _annuler(self):
        self.bouton_annuler.configure(state="disabled", text=self.t("recherche_en_cours.annulation"))
        self.app.moteur_recherche.annuler()

    def _rafraichir(self):
        if not self._actif:
            return
        etat = self.app.etat_progres
        traites = etat["traites"]
        dossier = etat["dossier_courant"]
        phase = etat.get("phase", "analyse")

        if traites > 0 or (phase == "parcours" and dossier):
            # Sur un dossier de départ large (C:\, profil utilisateur...),
            # le seul parcours des dossiers (avant même de lire un fichier)
            # peut prendre du temps : sans ce libellé distinct, l'écran
            # resterait figé sur "Parcours des dossiers…" sans aucun signe
            # de vie, alors même que l'app travaille toujours.
            cle = "recherche_en_cours.compteur_parcours" if phase == "parcours" else "recherche_en_cours.compteur"
            self.label_compteur.configure(text=self.t(cle, n=traites, dossier=tronquer_chemin(dossier)))
        self.after(150, self._rafraichir)
