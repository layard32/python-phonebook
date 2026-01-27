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
            style.configure("Treeview", font=("", 11))  

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
        
        btn_modifica = tk.Button(button_frame, text="Modifica", font=("", 12), command=self.edit_persona)
        btn_modifica.pack(side=tk.LEFT, padx=10)
        
        btn_elimina = tk.Button(button_frame, text="Elimina", font=("", 12), command=self.delete_persona)
        btn_elimina.pack(side=tk.LEFT, padx=10)
    

    # metodo per aggiornare la tabella con i dati della lista self.persone
    def update_table(self):
        # rimuovo tutte le righe
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # reinserisco i dati presi dalla lista delle persone
        for p in self.persone:
            self.tree.insert("", "end", values=(p.nome, p.cognome, p.telefono))


    # metodo per eliminare la persona selezionata dopo aver confermato
    def delete_persona(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Attenzione", "Seleziona una persona da eliminare.")
            return
        
        confirm = messagebox.askyesno("Conferma Eliminazione", "Sei sicuro di voler eliminare la persona selezionata?")
        if confirm:
            item_index = self.tree.index(selected_item)
            del self.persone[item_index]
            self.update_table()
            messagebox.showinfo("Successo", "Persona eliminata correttamente.")


    # metodo per modificare una persona
    def edit_persona(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Attenzione", "Seleziona una persona da modificare.")
            return
        # apro l'editor usato anche per creare una nuova persona, ma con i campi precompilati
        index = self.tree.index(selected_item)
        selected_persona = self.persone[index]
        self.open_editor(selected_persona)


    # creo la finestra per creare / modificare una persona
    def open_editor(self, selected_persona=None):    
        editor = tk.Toplevel(self.root)
        title = "Modifica Persona" if selected_persona else "Nuova Persona"
        editor.title(title)
        editor.geometry("360x400")
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
            
            # se la validazione è ok, creo o aggiorno la persona
            if selected_persona:
                # aggiorno i campi della persona esistente
                selected_persona.nome = nome
                selected_persona.cognome = cognome
                selected_persona.indirizzo = indirizzo
                selected_persona.telefono = telefono
                selected_persona.eta = int(eta_str)
            else:
                # creo una nuova persona e la aggiungo alla lista
                new_persona = Persona(nome, cognome, indirizzo, telefono, int(eta_str))
                self.persone.append(new_persona)
            
            # aggiorno e chiudo la finestra
            self.update_table() # Richiamo il metodo creato al punto 1
            editor.destroy()    # Chiudo la finestra
            messagebox.showinfo("Successo", "Contatto salvato correttamente!")


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
    root = tk.Tk()
    app = PhoneBookApp(root)
    root.mainloop()