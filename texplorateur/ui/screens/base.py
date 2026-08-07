import customtkinter as ctk


class Screen(ctk.CTkFrame):
    """Un écran de l'application, empilé dans le conteneur de contenu.

    `on_show`/`on_hide` sont des points d'extension appelés par le
    gestionnaire de navigation (`TexplorateurApp.navigate`) — les sous-classes
    les surchargent pour rafraîchir leur état à l'affichage.
    """

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app

    def on_show(self, **kwargs):
        pass

    def on_hide(self):
        pass
