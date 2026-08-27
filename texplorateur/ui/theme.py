import customtkinter as ctk

FONT_FAMILLE = "Segoe UI"

# Accent dédié à l'animation/statut de recherche : un teal qui se distingue
# du bleu des boutons d'action, plus sobre que le rose d'origine.
ACCENT_ANIMATION = "#4FD1C5"
ACCENT_SUCCES = "#3DAA5C"
ACCENT_ERREUR = "#E0555F"
ACCENT_GRIS = "gray"
ACCENT_LIEN = "#5B8DEF"
ACCENT_LIEN_SURVOL = "#4472D8"

PALETTE_CONFETTI = ["#4FD1C5", "#5B8DEF", "#F2B705", "#9D7FEF", "#F76E6E"]


def font_titre(size=22):
    return ctk.CTkFont(family=FONT_FAMILLE, size=size, weight="bold")


def font_sous_titre(size=13):
    return ctk.CTkFont(family=FONT_FAMILLE, size=size)


def font_normal(size=13, weight="normal"):
    return ctk.CTkFont(family=FONT_FAMILLE, size=size, weight=weight)
