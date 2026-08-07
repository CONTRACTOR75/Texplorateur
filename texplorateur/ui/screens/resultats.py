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
        ctk.CTkLabel(entete, text="Résultats de la recherche", font=font_titre(20)).pack(anchor='w')
        self.label_statut = ctk.CTkLabel(entete, text="", font=font_sous_titre(13))
        self.label_statut.pack(anchor='w', pady=(4, 0))

        boutons = ctk.CTkFrame(self, fg_color="transparent")
        boutons.pack(fill='x', padx=24, pady=(0, 8))
        ctk.CTkButton(boutons, text="+ Nouvelle recherche", command=lambda: self.app.navigate("formulaire")).pack(
            side='left')
        ctk.CTkButton(
            boutons, text="Accueil", fg_color="transparent", border_width=1,
            text_color=("gray10", "gray90"), command=lambda: self.app.navigate("accueil"),
        ).pack(side='left', padx=(8, 0))

        self.frame_resultats = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.frame_resultats.pack(fill='both', expand=True, padx=16, pady=(4, 16))

        self.label_tooltip = ctk.CTkLabel(self, text="", text_color="gray", font=font_sous_titre(11))
        self.label_tooltip.pack(fill='x', padx=24, pady=(0, 8))

    def on_show(self, resultats=None, total=0, **kwargs):
        resultats = resultats or []

        for widget in self.frame_resultats.winfo_children():
            widget.destroy()
        self.label_tooltip.configure(text="")

        if not resultats:
            self.label_statut.configure(
                text=f"Aucun résultat : la phrase n'apparaît dans aucun des {total} fichier(s) analysé(s).",
                text_color=ACCENT_ERREUR)
            return

        self.label_statut.configure(
            text=f"{len(resultats)} fichier(s) trouvé(s) sur {total} scanné(s)", text_color=ACCENT_SUCCES)
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
            entete, text="📂 Ouvrir", width=90,
            command=lambda c=chemin: [play_sound("open"), ouvrir_emplacement(c)],
        ).pack(side='right')

        if contexte:
            ctk.CTkLabel(
                carte, text=contexte, anchor='w', justify='left', text_color="gray", wraplength=760,
            ).pack(fill='x', padx=8, pady=(2, 8))
