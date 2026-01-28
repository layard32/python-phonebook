import os
import sys
from persona import Persona

class DataIo:
    def __init__(self):
        # dati salvati (cioè le persone) e nome della cartella
        self.persone = []
        self.data_folder_name = 'informazioni'
        # creo la cartella 
        self.data_folder_path = self._create_folder()
        

    # helper per la creazione della folder
    def _create_folder(self):
        base_path = self._get_path()
        folder_path = os.path.join(base_path, self.data_folder_name)
        if not os.path.exists(folder_path): # se non esiste, la creo
            os.makedirs(folder_path)
        return folder_path


    def _get_path(self):
        # controllo se il file è stato eseguito come script o come file exe
        # ed imposto il path della cartella di conseguenza
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        else:
            return os.path.dirname(os.path.abspath(__file__))
    

    # helper per ottenere il prossimo ID disponibile
    def _get_next_id(self):
        # se non esistono persone, il prossimo id è 1
        # altrimenti è il massimo id esistente + 1
        if not self.persone:
            return 1
        
        max_id = 0
        for persona in self.persone:
            if persona.id is not None and persona.id > max_id:
                max_id = persona.id
        return max_id + 1


    def update_data(self):
        # resetto la llista delle persone
        self.persone = []

        # se la cartella non esiste o è vuota, non faccio nulla
        if not os.path.exists(self.data_folder_path):
            return  

        # scansiono tutti i file nella cartella
        for filename in os.listdir(self.data_folder_path):
            # se il file è un txt e inizia con persona
            if filename.startswith("Persona") and filename.endswith('.txt'):
                try:
                    # estraggo l'id dal nome del file
                    file_id = int(filename.replace("Persona", "").replace(".txt", ""))
                    # ottengo la path del file
                    file_path = os.path.join(self.data_folder_path, filename)
                    # apro il file e faccio parsing dei dati
                    with open(file_path, 'r') as file:
                        content = file.read().strip()
                        if content: 
                            # i dati sono separati da punto e virgola
                            parts = content.split(';')
                            if len(parts) == 5:
                                persona = Persona(
                                    nome=parts[0],
                                    cognome=parts[1],
                                    indirizzo=parts[2],
                                    telefono=parts[3],
                                    eta=int(parts[4]),
                                    id=file_id
                                )
                                self.persone.append(persona)
                # se c'è un errore nell'apertura del file
                except Exception as e:
                    print(f"Errore nel caricamento del file {filename}: {e}")
        

    # metodi (gli unici pubblici) per salvare ed eliminare persone
    def save_persona(self, persona: Persona):
        # se la persona non ha un id, le assegno il prossimo disponibile
        if persona.id is None:
            persona.id = self._get_next_id()
        
        # creo il nome del file
        filename = f"Persona{persona.id}.txt"
        file_path = os.path.join(self.data_folder_path, filename)

        # scrivo i dati nel file con il formato specificato
        with open(file_path, 'w') as file:
            file.write(f"{persona.nome};{persona.cognome};{persona.indirizzo};{persona.telefono};{persona.eta}")

    def delete_persona(self, persona: Persona):
        # elimino il file e poi rimuovo dalla lista
        if persona.id is not None:
            filename = f"Persona{persona.id}.txt"
            file_path = os.path.join(self.data_folder_path, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        if persona in self.persone:
            self.persone.remove(persona)