from functions import app
"""from tkinter import Tk, Button, filedialog

def choisir_fichier():
    fichier = filedialog.askopenfilename(filetypes=[("Fichiers CSV, YAML, XML", "*.csv;*.yaml;*.xml")])
    # Traitez le fichier sélectionné ici

fenetre = Tk()
fenetre.title("Formateur de fichiers")

bouton_choisir = Button(fenetre, text="Choisir un fichier", command=choisir_fichier)
bouton_choisir.pack()

fenetre.mainloop()
"""


app('data/imported/file.csv', 'data/exported')