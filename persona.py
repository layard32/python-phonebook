# definisco la classe persona in base ai requisiti
class Persona:
    def __init__(self, nome: str, cognome: str, indirizzo: str, telefono: str, eta: int):
        self.nome = nome
        self.cognome = cognome
        self.indirizzo= indirizzo
        self.telefono = telefono
        self.eta = eta
    
    # per debugging
    def __print__(self):
        print(f"Nome: {self.nome}, Cognome: {self.cognome}, Indirizzo: {self.indirizzo}, Telefono: {self.telefono}, Età: {self.eta}")