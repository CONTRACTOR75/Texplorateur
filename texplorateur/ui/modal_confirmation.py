import customtkinter as ctk

from ..ressources import chemin_icone
from .theme import font_normal, font_titre


class ModalConfirmation(ctk.CTkToplevel):
    """Boîte de dialogue Oui/Non stylée comme le reste de l'app, plutôt que
    la messagebox native de l'OS (dont on ne maîtrise pas le texte des
    boutons ni l'apparence)."""

    def __init__(self, parent, titre, message, texte_oui, texte_non, on_confirmer):
        super().__init__(parent)
        self.title(titre)
        self.resizable(False, False)
        try:
            self.iconbitmap(chemin_icone())
        except Exception:
            pass

        self._on_confirmer = on_confirmer

        conteneur = ctk.CTkFrame(self, fg_color="transparent")
        conteneur.pack(padx=28, pady=24)

        ctk.CTkLabel(conteneur, text=titre, font=font_titre(15)).pack(pady=(0, 8))
        ctk.CTkLabel(
            conteneur, text=message, font=font_normal(13), wraplength=280, justify="center",
        ).pack(pady=(0, 20))

        boutons = ctk.CTkFrame(conteneur, fg_color="transparent")
        boutons.pack()
        ctk.CTkButton(
            boutons, text=texte_non, width=100, fg_color="transparent", border_width=1,
            text_color=("gray10", "gray90"), command=self._annuler,
        ).pack(side='left', padx=(0, 8))
        ctk.CTkButton(boutons, text=texte_oui, width=100, command=self._confirmer).pack(side='left')

        self.protocol("WM_DELETE_WINDOW", self._annuler)
        self.bind("<Escape>", lambda e: self._annuler())

        # Centrée sur la fenêtre parente, puis rendue modale une fois
        # positionnée (grab_set() avant que la fenêtre soit mappée échoue
        # silencieusement sous Windows).
        self.transient(parent)
        self.update_idletasks()
        self._centrer(parent)
        self.grab_set()
        self.focus_force()

    def _centrer(self, parent):
        largeur, hauteur = self.winfo_width(), self.winfo_height()
        x = parent.winfo_rootx() + (parent.winfo_width() - largeur) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - hauteur) // 2
        self.geometry(f"+{x}+{y}")

    def _confirmer(self):
        self.grab_release()
        self.destroy()
        self._on_confirmer()

    def _annuler(self):
        self.grab_release()
        self.destroy()
