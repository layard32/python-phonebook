# definisco la classe persona in base ai requisiti
class Persona:
    def __init__(self, nome: str, cognome: str, indirizzo: str, telefono: str, eta: int, id: int = None):
        self.nome = nome
        self.cognome = cognome
        self.indirizzo= indirizzo
        self.telefono = telefono
        self.eta = eta
        self.id = id
    
    # per debugging
    def __print__(self):
        print(f"Nome: {self.nome}, Cognome: {self.cognome}, ID: {self.id}")