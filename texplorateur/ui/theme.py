import customtkinter as ctk

FONT_FAMILLE = "Segoe UI"

# Toutes les couleurs d'accent sont des tuples (clair, sombre) : une chaîne
# unique donne la même couleur dans les deux thèmes, ce qui produit un
# contraste correct en sombre mais illisible en clair (vérifié : jusqu'à
# 1.2:1 sur fond clair pour le gris utilisé partout comme texte secondaire,
# très en dessous du seuil WCAG AA de 4.5:1). Chaque valeur ci-dessous garde
# la même teinte que l'original mais assombrie côté clair pour repasser
# ce seuil, sans changer l'apparence en sombre.

# Accent dédié à l'animation/statut de recherche : un teal qui se distingue
# du bleu des boutons d'action, plus sobre que le rose d'origine.
ACCENT_ANIMATION = ("#1B6760", "#4FD1C5")
ACCENT_SUCCES = ("#266A39", "#3DAA5C")
ACCENT_ERREUR = ("#B3212B", "#E46D75")
ACCENT_GRIS = ("gray30", "gray75")
ACCENT_LIEN = ("#1454D0", "#6292F0")
ACCENT_LIEN_SURVOL = ("#0D3EA8", "#4472D8")

PALETTE_CONFETTI = ["#4FD1C5", "#5B8DEF", "#F2B705", "#9D7FEF", "#F76E6E"]


def font_titre(size=22):
    return ctk.CTkFont(family=FONT_FAMILLE, size=size, weight="bold")


def font_sous_titre(size=13):
    return ctk.CTkFont(family=FONT_FAMILLE, size=size)


def font_normal(size=13, weight="normal"):
    return ctk.CTkFont(family=FONT_FAMILLE, size=size, weight=weight)
