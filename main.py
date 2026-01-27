from persona import Persona
import tkinter as tk
from tkinter import ttk, messagebox

# creo l'interfaccia grafica con tkinter
class PhoneBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rubrica Telefonica")
        self.root.geometry("800x600")
        
        # lista per memorizzare le persone
        self.persone = []
        
        # metodi per creare l'interfaccia, composta da tabella e bottoni
        self.create_table()
        self.create_buttons()

    # per la tabella utilizzo Treeview, che in teoria serve per mostrare alberi gerarchici
    # ma può essere usato anche per tabelle semplici grazie a show = "headings"
    def create_table(self):
            # mostro le tre tabelle come specificato nei requisiti
            required_columns = ("Nome", "Cognome", "Telefono")

            # configuro lo stile per gli heading con font più grande
            style = ttk.Style()
            style.configure("Treeview.Heading", font=("", 12))

            # creo l'oggetto Treeview per mostrare la tabella  
            self.tree = ttk.Treeview(self.root, columns=required_columns, show="headings")

            # configuro le intestazioni
            self.tree.heading("Nome", text="Nome")
            self.tree.heading("Cognome", text="Cognome")
            self.tree.heading("Telefono", text="Telefono")

            # configuro le colonne
            self.tree.column("Nome", width=200)
            self.tree.column("Cognome", width=200)
            self.tree.column("Telefono", width=200)

            # impacchetto dentro la finestra principale con padding e espansione
            self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


    # per i pulsanti utilizzo un contenitore Frame con dentro i Buttons
    def create_buttons(self):
        # contenitore orizzontale e in basso (centrato)
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.BOTTOM, padx=20, pady=20)

        # creo i tre bottoni TODO le azioni
        btn_nuovo = tk.Button(button_frame, text="Nuovo", font=("", 12), command=self.open_editor)
        btn_nuovo.pack(side=tk.LEFT, padx=10)
        
        btn_modifica = tk.Button(button_frame, text="Modifica", font=("", 12))
        btn_modifica.pack(side=tk.LEFT, padx=10)
        
        btn_elimina = tk.Button(button_frame, text="Elimina", font=("", 12))
        btn_elimina.pack(side=tk.LEFT, padx=10)
    

    def open_editor(self):
        # creo la finestra per creare / modificare una persona
        editor = tk.Toplevel(self.root)
        editor.title("Editor Persona")
        editor.geometry("360x400")
        editor.resizable(False, False)
        # per bloccare l'interazione con la finestra principale
        editor.grab_set()
        # utilizzo grid per disporre i campi in modo ordinato
        labels = ["Nome", "Cognome", "Indirizzo", "Telefono", "Età"]
        self.entries = {} # dizionario per tenere traccia dei campi di input
        for i, label in enumerate(labels):
            # aggiungo padding superiore maggiore solo per la prima riga
            pady_value = (30, 10) if i == 0 else 10
            tk.Label(editor, text=label, font=("", 12)).grid(row=i, column=0, padx=10, pady=pady_value, sticky=tk.W)
            entry = tk.Entry(editor, font=("", 12), width=25)
            entry.grid(row=i, column=1, padx=10, pady=pady_value)
            self.entries[label] = entry

        # configurare la griglia per espandere lo spazio prima dei pulsanti
        editor.grid_rowconfigure(len(labels), weight=1)

        # dispongo i pulsanti Salva e Annulla nella parte più bassa della finestra
        button_frame = tk.Frame(editor)
        button_frame.grid(row=len(labels)+1, column=0, columnspan=2, pady=20, sticky=tk.S)
        # TODO implementazione azione salvataggio
        btn_salva = tk.Button(button_frame, text="Salva", font=("", 12), width=10)
        btn_salva.pack(side=tk.LEFT, padx=10)
        # annulla chiude semplicemente l'editor senza salvare o fare nulla
        btn_annulla = tk.Button(button_frame, text="Annulla", font=("", 12), width=10, command=editor.destroy)
        btn_annulla.pack(side=tk.LEFT, padx=10)



# avvio l'applicazione
if __name__ == "__main__":
    root = tk.Tk()
    app = PhoneBookApp(root)
    root.mainloop()