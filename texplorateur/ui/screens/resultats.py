import customtkinter as ctk

from ...explorateur import ouvrir_emplacement
from ...son import play_sound
from ..confetti import ConfettiCanvas
from ..theme import ACCENT_ERREUR, ACCENT_SUCCES, font_normal, font_sous_titre, font_titre
from .base import Screen


class ResultatsScreen(Screen):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        self.confetti_canvas = ConfettiCanvas(self, color_ref=app.root, height=50)
        self.confetti_canvas.pack(fill='x')

        entete = ctk.CTkFrame(self, fg_color="transparent")
        entete.pack(fill='x', padx=24, pady=(8, 4))
        self.label_titre = ctk.CTkLabel(entete, text=self.t("resultats.titre"), font=font_titre(20))
        self.label_titre.pack(anchor='w')
        self.label_statut = ctk.CTkLabel(entete, text="", font=font_sous_titre(13))
        self.label_statut.pack(anchor='w', pady=(4, 0))

        boutons = ctk.CTkFrame(self, fg_color="transparent")
        boutons.pack(fill='x', padx=24, pady=(0, 8))
        self.bouton_nouvelle_recherche = ctk.CTkButton(
            boutons, text=self.t("commun.nouvelle_recherche"), command=lambda: self.app.navigate("formulaire"))
        self.bouton_nouvelle_recherche.pack(side='left')
        self.bouton_accueil = ctk.CTkButton(
            boutons, text=self.t("commun.accueil"), fg_color="transparent", border_width=1,
            text_color=("gray10", "gray90"), command=lambda: self.app.navigate("accueil"),
        )
        self.bouton_accueil.pack(side='left', padx=(8, 0))

        self.frame_resultats = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.frame_resultats.pack(fill='both', expand=True, padx=16, pady=(4, 16))

        self.label_tooltip = ctk.CTkLabel(self, text="", text_color="gray", font=font_sous_titre(11))
        self.label_tooltip.pack(fill='x', padx=24, pady=(0, 8))

    def retraduire(self):
        self.label_titre.configure(text=self.t("resultats.titre"))
        self.bouton_nouvelle_recherche.configure(text=self.t("commun.nouvelle_recherche"))
        self.bouton_accueil.configure(text=self.t("commun.accueil"))

    def on_show(self, resultats=None, total=0, silencieux=False, **kwargs):
        resultats = resultats or []

        for widget in self.frame_resultats.winfo_children():
            widget.destroy()
        self.label_tooltip.configure(text="")

        if not resultats:
            self.label_statut.configure(
                text=self.t("resultats.aucun_resultat", total=total), text_color=ACCENT_ERREUR)
            return

        self.label_statut.configure(
            text=self.t("resultats.trouves", n=len(resultats), total=total), text_color=ACCENT_SUCCES)

        # `silencieux` : consultation d'un résultat déjà archivé depuis
        # l'historique — pas de fanfare, ce n'est pas une nouvelle trouvaille.
        if not silencieux:
            play_sound("success")
            self.after(150, self.confetti_canvas.throw_confetti)

        for nom_fichier, chemin, contexte in resultats:
            self._afficher_resultat(nom_fichier, chemin, contexte)

    def _afficher_resultat(self, nom_fichier, chemin, contexte):
        carte = ctk.CTkFrame(self.frame_resultats)
        carte.pack(fill='x', padx=4, pady=4)

        entete = ctk.CTkFrame(carte, fg_color="transparent")
        entete.pack(fill='x', padx=8, pady=(6, 0))

        label = ctk.CTkLabel(entete, text=nom_fichier, anchor='w', font=font_normal(13, "bold"))
        label.pack(side='left', fill='x', expand=True)
        label.bind("<Enter>", lambda e, c=chemin: self.label_tooltip.configure(text=c))
        label.bind("<Leave>", lambda e: self.label_tooltip.configure(text=""))

        ctk.CTkButton(
            entete, text=self.t("commun.ouvrir"), width=90,
            command=lambda c=chemin: [play_sound("open"), ouvrir_emplacement(c)],
        ).pack(side='right')

        if contexte:
            ctk.CTkLabel(
                carte, text=contexte, anchor='w', justify='left', text_color="gray", wraplength=760,
            ).pack(fill='x', padx=8, pady=(2, 8))
