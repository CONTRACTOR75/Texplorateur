import itertools

import customtkinter as ctk

from ..son import play_sound
from .theme import ACCENT_ANIMATION, font_normal

LOADER_CHARS = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']


class CuteAnimation:
    """Indicateur d'activité animé, affiché pendant une recherche."""

    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")

        self.label_loader = ctk.CTkLabel(
            self.frame, text="", font=ctk.CTkFont(size=32), text_color=ACCENT_ANIMATION,
        )
        self.label_loader.pack()

        self.label_message = ctk.CTkLabel(
            self.frame, text="", font=font_normal(14), text_color=ACCENT_ANIMATION,
        )
        self.label_message.pack(pady=(4, 0))

        self._messages = None
        self._loader_chars = itertools.cycle(LOADER_CHARS)
        self.is_running = False

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def pack_forget(self):
        self.frame.pack_forget()

    def start(self):
        self.is_running = True
        # Reconstruit le cycle des messages à chaque lancement plutôt qu'une
        # fois pour toutes : reflète la langue courante même si elle a
        # changé depuis la construction du widget.
        messages = self.app.i18n.t("recherche_en_cours.messages")
        self._messages = itertools.cycle(messages if isinstance(messages, list) else [messages])
        play_sound("start")
        self._animate()

    def stop(self):
        self.is_running = False

    def _animate(self):
        if not self.is_running:
            return
        self.label_loader.configure(text=next(self._loader_chars))
        self.label_message.configure(text=next(self._messages))
        self.parent.after(180, self._animate)
