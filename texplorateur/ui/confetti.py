import random
import tkinter as tk

from .theme import PALETTE_CONFETTI


class ConfettiCanvas(tk.Canvas):
    def __init__(self, parent, color_ref=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg=self._fond(color_ref or parent), highlightthickness=0)
        self.colors = PALETTE_CONFETTI
        self.shapes = ['circle', 'square', 'triangle']

    def _fond(self, widget):
        try:
            fg = widget.cget('fg_color')
            couleur = fg[1] if isinstance(fg, (list, tuple)) else fg
            # "transparent" n'est pas une couleur valide pour un tk.Canvas classique.
            if not couleur or couleur == "transparent":
                raise ValueError
            return couleur
        except Exception:
            return "#1a1a1a"

    def throw_confetti(self):
        self.delete('all')
        width = self.winfo_width()
        height = self.winfo_height()

        for _ in range(50):
            x = random.randint(0, max(width, 1))
            y = random.randint(-50, 0)
            size = random.randint(5, 15)
            color = random.choice(self.colors)
            shape = random.choice(self.shapes)

            if shape == 'circle':
                self.create_oval(x, y, x + size, y + size, fill=color, outline="")
            elif shape == 'square':
                self.create_rectangle(x, y, x + size, y + size, fill=color, outline="")
            else:
                self.create_polygon(x, y, x + size, y, x + size / 2, y - size, fill=color, outline="")

        self.animate_confetti(height)

    def animate_confetti(self, max_y):
        for item in self.find_all():
            y = self.coords(item)[1]
            speed = random.uniform(0.5, 2.5)
            new_y = y + speed

            if new_y < max_y + 50:
                self.move(item, 0, speed)
            else:
                self.move(item, 0, -max_y - 100)

        self.after(20, lambda: self.animate_confetti(max_y))
