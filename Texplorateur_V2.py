import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import docx
import PyPDF2
import threading
import random
import winsound
from PIL import Image, ImageTk
import itertools

# Configuration des sons (Windows seulement)
def play_sound(sound_type):
    try:
        if sound_type == "start":
            winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC)
        elif sound_type == "success":
            winsound.PlaySound("SystemExclamation", winsound.SND_ASYNC)
        elif sound_type == "open":
            winsound.PlaySound("SystemHand", winsound.SND_ASYNC)
    except:
        pass  # Silencieux si les sons ne fonctionnent pas

# Système de confetti
class ConfettiCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg=parent.cget('bg'), highlightthickness=0)
        self.colors = ['#FF6B9E', '#6B9EFF', '#9EFF6B', '#FFD96B', '#D96BFF']
        self.shapes = ['circle', 'square', 'triangle']
    
    def throw_confetti(self):
        self.delete('all')
        width = self.winfo_width()
        height = self.winfo_height()
        
        for _ in range(50):
            x = random.randint(0, width)
            y = random.randint(-50, 0)
            size = random.randint(5, 15)
            color = random.choice(self.colors)
            shape = random.choice(self.shapes)
            
            if shape == 'circle':
                self.create_oval(x, y, x+size, y+size, fill=color, outline="")
            elif shape == 'square':
                self.create_rectangle(x, y, x+size, y+size, fill=color, outline="")
            else:  # triangle
                self.create_polygon(x, y, x+size, y, x+size/2, y-size, fill=color, outline="")
        
        self.animate_confetti(height)
    
    def animate_confetti(self, max_y):
        for item in self.find_all():
            x, y = self.coords(item)[0], self.coords(item)[1]
            speed = random.uniform(0.5, 2.5)
            new_y = y + speed
            
            if new_y < max_y + 50:
                self.move(item, 0, speed)
            else:
                self.move(item, 0, -max_y - 100)
        
        self.after(20, lambda: self.animate_confetti(max_y))

# Animation mignonne
class CuteAnimation:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, bg=parent.cget('bg'))
        self.label = tk.Label(self.frame, font=('Arial', 12), fg="#FF6B9E", bg=parent.cget('bg'))
        self.label.pack()
        
        self.emoji_sequence = itertools.cycle([
            "🔍 Cherche dans les fichiers...", 
            "📂 Parcourt les dossiers...", 
            "📖 Analyse le contenu...", 
            "✨ Presque fini...",
            "💖 Patiente un peu..."
        ])
        
        self.loader_chars = itertools.cycle(['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷'])
        self.is_running = False
    
    def start(self):
        self.is_running = True
        self.frame.pack(pady=10)
        play_sound("start")
        self.animate()
    
    def stop(self):
        self.is_running = False
        self.frame.pack_forget()
    
    def animate(self):
        if self.is_running:
            emoji = next(self.emoji_sequence)
            loader = next(self.loader_chars)
            self.label.config(text=f"{loader} {emoji}")
            self.parent.after(300, self.animate)

def lire_txt(chemin):
    try:
        with open(chemin, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except:
        return ""

def lire_docx(chemin):
    try:
        doc = docx.Document(chemin)
        return '\n'.join([p.text for p in doc.paragraphs])
    except:
        return ""

def lire_pdf(chemin):
    try:
        texte = ""
        with open(chemin, 'rb') as f:
            lecteur = PyPDF2.PdfReader(f)
            for page in lecteur.pages:
                texte += page.extract_text() or ""
        return texte
    except:
        return ""

def rechercher_en_thread():
    phrase = champ_phrase.get().strip()
    extension = extension_var.get()
    dossier = filedialog.askdirectory(title="Choisir le dossier de départ")

    if not phrase or not extension or not dossier:
        messagebox.showwarning("Champs requis", "Veuillez remplir tous les champs.")
        return

    bouton_recherche.config(state=tk.DISABLED)
    cute_animation.start()  # Correction: Utilisation de l'instance

    def thread_task():
        resultats = []
        total_fichiers = 0
        
        for dossier_courant, _, fichiers in os.walk(dossier):
            for fichier in fichiers:
                if fichier.lower().endswith(extension):
                    total_fichiers += 1
                    chemin = os.path.join(dossier_courant, fichier)
                    contenu = ""
                    
                    if extension == ".txt":
                        contenu = lire_txt(chemin)
                    elif extension == ".docx":
                        contenu = lire_docx(chemin)
                    elif extension == ".pdf":
                        contenu = lire_pdf(chemin)

                    if phrase.lower() in contenu.lower():
                        resultats.append((fichier, chemin))
        
        racine.after(0, lambda: afficher_resultats(resultats, total_fichiers))

    threading.Thread(target=thread_task, daemon=True).start()

def afficher_resultats(fichiers, total_fichiers):
    cute_animation.stop()  # Correction: Utilisation de l'instance
    bouton_recherche.config(state=tk.NORMAL)

    for widget in frame_resultats.winfo_children():
        widget.destroy()
    
    if not fichiers:
        label_statut.config(text=f"Aucun fichier trouvé (scannés: {total_fichiers})", fg="red")
        return
    
    play_sound("success")
    confetti_canvas.throw_confetti()  # Correction: Faute de frappe corrigée
    label_statut.config(text=f"{len(fichiers)} fichiers trouvés (sur {total_fichiers})", fg="green")
    
    # Créer un cadre pour l'en-tête
    header_frame = tk.Frame(frame_resultats, bg="#f0f0f0")
    header_frame.pack(fill='x', pady=(0, 5))
    
    tk.Label(header_frame, text="Fichiers trouvés", bg="#f0f0f0", font=('Arial', 10, 'bold')).pack(side='left', padx=5)
    
    # Afficher chaque fichier trouvé
    for nom_fichier, chemin in fichiers:
        ligne = tk.Frame(frame_resultats)
        ligne.pack(fill='x', padx=5, pady=2)
        
        # Nom du fichier avec tooltip
        label = tk.Label(ligne, text=nom_fichier, anchor='w')
        label.pack(side='left', fill='x', expand=True)
        
        def make_lambda(path):
            return lambda e: label_tooltip.config(text=path)
        
        label.bind("<Enter>", make_lambda(chemin))
        label.bind("<Leave>", lambda e: label_tooltip.config(text=""))
        
        # Bouton pour ouvrir l'emplacement du fichier
        btn = tk.Button(ligne, text="📂", command=lambda c=chemin: [play_sound("open"), ouvrir_emplacement(c)],
                    relief=tk.FLAT, bd=0)
        btn.pack(side='right')

def ouvrir_emplacement(chemin):
    try:
        chemin_normalise = os.path.normpath(chemin)
        if os.name == 'nt':  # Windows
            subprocess.Popen(f'explorer /select,"{chemin_normalise}"')
        else:  # Mac/Linux
            dossier = os.path.dirname(chemin_normalise)
            subprocess.Popen(['xdg-open', dossier])
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'ouvrir l'explorateur: {str(e)}")

# Interface utilisateur
racine = tk.Tk()
racine.title("Texplorateur")
racine.geometry("800x600")  # Augmenté la hauteur pour le confetti

# Style
style = ttk.Style()
style.configure('TCombobox', padding=5)
style.configure('TButton', padding=5)

# Création des éléments d'animation
confetti_canvas = ConfettiCanvas(racine, height=50)
confetti_canvas.pack(fill='x')
cute_animation = CuteAnimation(racine)  # Création de l'instance

# Cadre principal
main_frame = tk.Frame(racine, padx=10, pady=10)
main_frame.pack(fill='both', expand=True)

# Champ de recherche
tk.Label(main_frame, text="Phrase à rechercher :").pack(anchor='w')
champ_phrase = tk.Entry(main_frame, width=80)
champ_phrase.pack(fill='x', pady=(0, 10))

# Sélection d'extension
tk.Label(main_frame, text="Type de fichier :").pack(anchor='w')
extension_var = tk.StringVar()
liste_extensions = ttk.Combobox(main_frame, textvariable=extension_var, 
                              values=[".txt", ".pdf", ".docx"], 
                              state="readonly", width=10)
liste_extensions.pack(anchor='w', pady=(0, 10))
liste_extensions.current(0)

# Bouton de recherche
bouton_recherche = ttk.Button(main_frame, text="Rechercher", command=rechercher_en_thread)
bouton_recherche.pack(pady=5)

# Label de statut
label_statut = tk.Label(main_frame, text="", font=('Arial', 9))
label_statut.pack()

# Label pour tooltip
label_tooltip = tk.Label(main_frame, text="", fg="gray", font=('Arial', 8))
label_tooltip.pack(fill='x')

# Zone de résultats avec scrollbar
result_frame = tk.Frame(main_frame)
result_frame.pack(fill='both', expand=True)

canvas = tk.Canvas(result_frame)
scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

frame_resultats = scrollable_frame

racine.mainloop()