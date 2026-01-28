import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk 

class LoginWindow(ttk.Toplevel):
    def __init__(self, parent):
        # chiamo il costruttore della classe base
        super().__init__(parent)

        # stile
        self.geometry("330x300")
        self.resizable(False, False)
        self.title("Login - Rubrica Telefonica")
        self.place_window_center()

        # variabile per comunicare il risultato del login al parent
        self.login_successful = False

        # creo il form di login
        self._create_form() 

        # per sicurezza, faccio sì che la variabile venga settata a False se la finestra viene chiusa
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    
    def _create_form(self):
        # username
        ttk.Label(self, text="🔐 Accesso Richiesto", font=("", 14, "bold")).pack(pady=20)
        ttk.Label(self, text="Username").pack()
        self.user_entry = ttk.Entry(self)
        self.user_entry.pack(pady=5)
        self.user_entry.focus()

        # password
        ttk.Label(self, text="Password").pack()
        self.pass_entry = ttk.Entry(self, show="*")
        self.pass_entry.pack(pady=5)
        
        # tasto invio e pulsante per il lgoin
        self.pass_entry.bind("<Return>", lambda e: self._check_login())
        btn_login = ttk.Button(self, text="Login", command=self._check_login, bootstyle="primary")
        btn_login.pack(pady=20, ipadx=10)

    
    # logica per il login
    def _check_login(self):
        # prendo i dati dal form
        user = self.user_entry.get()
        password = self.pass_entry.get()

        # controllo se i dati sono corretti
        # PER ORA SONO HARD-CODED, MA POSSO IMPLEMENTARE UN SISTEMA DI GESTIONE UTENTI IN FUTURO
        if user == "admin" and password == "password":
            self.login_successful = True
            self.destroy()
        else:
            messagebox.showerror("Errore di Login", "Username o Password errati. Riprova.")
        

    def _on_close(self):
        self.login_successful = False
        self.destroy()