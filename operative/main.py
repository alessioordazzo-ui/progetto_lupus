import random

# 1. Configurazione iniziale del gioco
# Questa lista di ruoli verrà assegnata casualmente ai giocatori
RUOLI_DISPONIBILI = ["Lupo", "Lupo", "Veggente", "Medico", "Contadino", "Contadino", "Contadino"]

# Lista dei giocatori che si sono connessi alla stanza
giocatori_connessi = ["Alice", "Bob", "Carlo", "Diana", "Elena", "Fabio", "Giorgio"]

# Dizionario che conterrà la partita: { "NomeGiocatore": {"ruolo": "...", "vivo": True} }
partita = {}

# --- FASE 1: ASSEGNAZIONE CASUALE DEI RUOLI ---
def assegna_ruoli():
    # Mescoliamo la lista dei ruoli in modo casuale
    random.shuffle(RUOLI_DISPONIBILI)
    
    # Associamo ogni giocatore a un ruolo mescolato
    for i in range(len(giocatori_connessi)):
        nome_giocatore = giocatori_connessi[i]
        ruolo_assegnato = RUOLI_DISPONIBILI[i]
        
        partita[nome_giocatore] = {
            "ruolo": ruolo_assegnato,
            "vivo": True
        }

# --- FASE 2: SCHERMATA DEL NARRATORE (Pannello di Controllo) ---
def mostra_schermata_narratore():
    print("\n--- PANNELLO DEL NARRATORE (Vedi solo tu!) ---")
    for nome, info in partita.items():
        stato = "VIVO" if info["vivo"] else "MORTO"
        print(f"Giocatore: {nome} | Ruolo: {info['ruolo']} | Stato: {stato}")
    print("---------------------------------------------\n")

# --- FASE 3: L'AZIONE DEL NARRATORE (Linciare/Eliminare un giocatore) ---
def lincia_giocatore(nome_bersaglio):
    if nome_bersaglio in partita:
        if partita[nome_bersaglio]["vivo"]:
            partita[nome_bersaglio]["vivo"] = False
            print(f"💥 Il Narratore ha lynchato {nome_bersaglio}! Era un {partita[nome_bersaglio]['ruolo']}.")
        else:
            print(f"⚠️ {nome_bersaglio} è già morto!")
    else:
        print("⚠️ Giocatore non trovato nella stanza.")

# --- SIMULAZIONE DELLA PARTITA ---

# Il Narratore avvia la partita: l'app assegna i ruoli
assegna_ruoli()

# Il Narratore guarda la sua schermata segreta per guidare il gioco a voce
mostra_schermata_narratore()

# Esempio: i giocatori votano a voce, decidono di eliminare "Bob"
# Il Narratore preme il pulsante sul suo telefono per eliminare Bob
lincia_giocatore("Bob")

# Il Narratore controlla la schermata aggiornata per vedere chi è rimasto
mostra_schermata_narratore()