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

    def t(self, cle, **kwargs):
        return self.app.i18n.t(cle, **kwargs)

    def on_show(self, **kwargs):
        pass

    def on_hide(self):
        pass

    def retraduire(self):
        """Appelé par l'app quand la langue change : à surcharger pour
        remettre à jour les textes statiques créés une seule fois en
        __init__ (titres, libellés, boutons). Le contenu dynamique
        (compteurs, résultats...) n'a pas besoin d'être traité ici — il est
        recalculé dans la langue courante au prochain `on_show`."""
        pass
