import customtkinter as ctk

from ...readers import tronquer_chemin
from ..cute_animation import CuteAnimation
from ..theme import font_sous_titre
from .base import Screen


class RechercheEnCoursScreen(Screen):
    """Écran plein cadre affiché pendant une recherche : rien d'autre à l'écran."""

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._actif = False

        centre = ctk.CTkFrame(self, fg_color="transparent")
        centre.place(relx=0.5, rely=0.46, anchor="center")

        self.cute_animation = CuteAnimation(centre)
        self.cute_animation.pack()

        self.barre = ctk.CTkProgressBar(centre, mode="indeterminate", width=280)
        self.barre.pack(pady=(20, 8))

        self.label_compteur = ctk.CTkLabel(centre, text="", font=font_sous_titre(11), text_color="gray")
        self.label_compteur.pack()

        self.bouton_annuler = ctk.CTkButton(
            centre, text="Annuler", fg_color="transparent", border_width=1,
            text_color=("gray10", "gray90"), command=self._annuler,
        )
        self.bouton_annuler.pack(pady=(24, 0))

    def on_show(self, **kwargs):
        self._actif = True
        self.bouton_annuler.configure(state="normal", text="Annuler")
        self.label_compteur.configure(text="Parcours des dossiers…")
        self.cute_animation.start()
        self.barre.start()
        self._rafraichir()

    def on_hide(self):
        self._actif = False
        self.cute_animation.stop()
        self.barre.stop()

    def _annuler(self):
        self.bouton_annuler.configure(state="disabled", text="Annulation…")
        self.app.moteur_recherche.annuler()

    def _rafraichir(self):
        if not self._actif:
            return
        etat = self.app.etat_progres
        traites = etat["traites"]
        dossier = etat["dossier_courant"]
        if traites > 0:
            self.label_compteur.configure(text=f"{traites} fichier(s) analysé(s) — {tronquer_chemin(dossier)}")
        self.after(150, self._rafraichir)
