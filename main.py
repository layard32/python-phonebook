from persona import Persona
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from data_io import DataIo

# creo l'interfaccia grafica con tkinter
class PhoneBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rubrica Telefonica")
        self.root.geometry("800x600")

        # configurazione di stile extra per la toolbar e UI
        style = ttk.Style()
        style.configure("Toolbar.TFrame", background="#e9ecef", borderwidth=0, relief="flat")
        style.configure(
            "Toolbar.TButton",
            font=("Segoe UI", 10),
            padding=(10, 6),
        )
        style.map(
            "Toolbar.TButton",
            foreground=[("disabled", "#9aa0a6")],
        )
        style.configure("Treeview.Heading", font=("Segoe UI Semibold", 11))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)

        # io gestisce i dati
        self.io_handler = DataIo()
        
        # metodi per creare l'interfaccia, composta da toolbar e tabela
        self.create_toolbar()

        # contenitore principale con padding per un look più arioso
        content = ttk.Frame(self.root, padding=(12, 8, 12, 12))
        content.pack(fill=tk.BOTH, expand=True)
        self.content = content

        self.create_table()

        # all'apertura dell'app aggiorna subito i dati
        self.io_handler.update_data()
        self.update_table()


    # per la tabella utilizzo Treeview, che in teoria serve per mostrare alberi gerarchici
    # ma può essere usato anche per tabelle semplici grazie a show = "headings"
    def create_table(self):
            # mostro le tre tabelle come specificato nei requisiti
            required_columns = ("Nome", "Cognome", "Telefono")

            # creo l'oggetto Treeview per mostrare la tabella  
            self.tree = ttk.Treeview(self.content, columns=required_columns, show="headings")

            # configuro le intestazioni
            self.tree.heading("Nome", text="Nome")
            self.tree.heading("Cognome", text="Cognome")
            self.tree.heading("Telefono", text="Telefono")

            # configuro le colonne
            self.tree.column("Nome", width=200)
            self.tree.column("Cognome", width=200)
            self.tree.column("Telefono", width=200)

            # impacchetto dentro il contenitore principale con padding e espansione
            self.tree.pack(fill=tk.BOTH, expand=True)


    # per i pulsanti utilizzo una toolbar con i pulsanti
    def create_toolbar(self):
        # stile della toolbar
        toolbar = ttk.Frame(self.root, style="Toolbar.TFrame", padding=(8, 6))
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # uso le emoji per avere delle icone senza gestire immagini
        btn_nuovo = ttk.Button(toolbar, text="➕ Nuovo", style="Toolbar.TButton", command=lambda: self.open_editor(None))
        btn_nuovo.pack(side=tk.LEFT, padx=4, pady=2)
        
        btn_modifica = ttk.Button(toolbar, text="✏️ Modifica", style="Toolbar.TButton", command=self.edit_persona)
        btn_modifica.pack(side=tk.LEFT, padx=4, pady=2)
        
        btn_elimina = ttk.Button(toolbar, text="🗑️ Elimina", style="Toolbar.TButton", command=self.delete_persona)
        btn_elimina.pack(side=tk.LEFT, padx=4, pady=2)
    

    # metodo per aggiornare la tabella con i dati della lista self.persone
    def update_table(self):
        # rimuovo tutte le righe
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # reinserisco i dati presi dall'io handler
        for p in self.io_handler.persone:
            self.tree.insert("", "end", values=(p.nome, p.cognome, p.telefono))


    # metodo per eliminare la persona selezionata dopo aver confermato
    def delete_persona(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Attenzione", "Seleziona una persona da eliminare.")
            return
        
        confirm = messagebox.askyesno("Conferma Eliminazione", "Sei sicuro di voler eliminare la persona selezionata?")
        if confirm:
            # cancello tramite l'io handler, che richiede in input la persona
            persona_index = self.tree.index(selected_item[0])
            persona_to_delete = self.io_handler.persone[persona_index]

            try:
                self.io_handler.delete_persona(persona_to_delete)
                # aggiorno la tabella
                self.update_table()
                messagebox.showinfo("Successo", "Persona eliminata correttamente.")
            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile eliminare: {e}")


    # metodo per modificare una persona
    def edit_persona(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Attenzione", "Seleziona una persona da modificare.")
            return
        # apro l'editor usato anche per creare una nuova persona, ma con i campi precompilati
        index = self.tree.index(selected_item[0])
        selected_persona = self.io_handler.persone[index]
        self.open_editor(selected_persona)


    # creo la finestra per creare / modificare una persona
    # l'argomento opzionale selected_persona indica se sto modificando una persona esistente
    def open_editor(self, selected_persona=None):    
        editor = tk.Toplevel(self.root)
        title = "Modifica Persona" if selected_persona else "Nuova Persona"
        editor.title(title)
        editor.geometry("430x430")
        editor.resizable(False, False)
        editor.grab_set() # per bloccare l'interazione con la finestra principale

        labels = ["Nome", "Cognome", "Indirizzo", "Telefono", "Età"]
        self.entries = {} # dizionario per tenere traccia dei campi di input

        for i, label in enumerate(labels):
            pady_value = (30, 10) if i == 0 else 10
            tk.Label(editor, text=label, font=("", 12)).grid(row=i, column=0, padx=10, pady=pady_value, sticky=tk.W)

            entry = tk.Entry(editor, font=("", 12), width=25)
            entry.grid(row=i, column=1, padx=10, pady=pady_value)
            self.entries[label] = entry

        # se sto modificando precompilo i campi
        if selected_persona:
            self.entries["Nome"].insert(0, selected_persona.nome)
            self.entries["Cognome"].insert(0, selected_persona.cognome)
            self.entries["Indirizzo"].insert(0, selected_persona.indirizzo)
            self.entries["Telefono"].insert(0, selected_persona.telefono)
            self.entries["Età"].insert(0, selected_persona.eta)

        editor.grid_rowconfigure(len(labels), weight=1)

        # definisco come nested function la logica di salvataggio
        # questo metodo richiama il metodo dentro l'io per salvare effettivamente la persona
        # qua si fa soltanto parsing e validazione dei dati
        def save_persona():
            # estraggo i dati da self.entries
            nome = self.entries["Nome"].get()
            cognome = self.entries["Cognome"].get()
            indirizzo = self.entries["Indirizzo"].get()
            telefono = self.entries["Telefono"].get()
            eta_str = self.entries["Età"].get()

            # validazione dei dati
            if not nome or not cognome or not telefono:
                # presuppongo siano obbligatori poiché mostrati nella tabella principale
                messagebox.showerror("Errore", "Nome, Cognome e Telefono sono obbligatori!")
                return 
            
            # Controllo che l'età sia un numero e intero
            if not eta_str.isdigit():
                 messagebox.showerror("Errore", "L'età deve essere un numero intero!")
                 return

            # controllo il telefono sia composto solo da numeri
            if not telefono.isdigit():
                messagebox.showerror("Errore", "Il numero di telefono deve contenere solo cifre!")
                return
            
            try:
                if selected_persona:
                    # se si sta modificando
                    selected_persona.nome = nome
                    selected_persona.cognome = cognome
                    selected_persona.indirizzo = indirizzo
                    selected_persona.telefono = telefono
                    selected_persona.eta = int(eta_str)
                    # il manager sovrascriverà il file esistente con i nuovi dati
                    self.io_handler.save_persona(selected_persona)
                else:
                    # se si sta creando una nuova persona
                    new_persona = Persona(nome, cognome, indirizzo, telefono, int(eta_str))
                    self.io_handler.save_persona(new_persona)
                
                # ricarico i dati dai file e aggiorno la tabella
                self.io_handler.update_data()
                self.update_table()
                editor.destroy()
                messagebox.showinfo("Successo", "Dati salvati!")
            
            except Exception as e:
                messagebox.showerror("Errore durante il salvataggio", str(e))

        # dispongo i pulsanti Salva e Annulla nella parte più bassa della finestra
        # annulla chiude la finestra senza fare nulla, salva richiama la nested function save_persona
        button_frame = tk.Frame(editor)
        button_frame.grid(row=len(labels)+1, column=0, columnspan=2, pady=20, sticky=tk.S)

        btn_salva_label = "Modifica" if selected_persona else "Salva"
        btn_salva = tk.Button(button_frame, text=btn_salva_label, font=("", 12), width=10, command=save_persona)
        btn_salva.pack(side=tk.LEFT, padx=10)

        btn_annulla = tk.Button(button_frame, text="Annulla", font=("", 12), width=10, command=editor.destroy)
        btn_annulla.pack(side=tk.LEFT, padx=10)

    

# avvio l'applicazione
if __name__ == "__main__":
    root = ttk.Window(themename="cosmo") 
    app = PhoneBookApp(root)
    root.mainloop()