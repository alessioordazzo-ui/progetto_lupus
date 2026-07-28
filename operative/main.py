import random
from ruoli import RUOLI_SPECIALI  # legge i dati da ruoli.json

# 1. Configurazione iniziale del gioco
# Qui decidi QUANTI ruoli speciali vuoi in partita (i nomi devono esistere
# in ruoli.json, altrimenti il programma ti avvisa subito con un errore chiaro).
# Tutti i posti rimanenti vengono riempiti automaticamente con "Contadino".
COMPOSIZIONE_RUOLI = {
    "Veggente": 1,
    "Medico": 1,
    "Lupo Silenziatore": 2,
}

# Lista dei giocatori che si sono connessi alla stanza
giocatori_connessi = ["Alice", "Bob", "Carlo", "Diana", "Elena", "Fabio", "Giorgio"]

# Dizionario che conterrà la partita: { "NomeGiocatore": {"ruolo": "...", "vivo": True} }
partita = {}


# --- FASE 0: CONTROLLO CHE LA COMPOSIZIONE ABBIA SENSO ---
def costruisci_lista_ruoli(numero_giocatori):
    """Costruisce la lista dei ruoli da assegnare, partendo da COMPOSIZIONE_RUOLI
    e riempiendo i posti restanti con 'Contadino'."""

    lista_ruoli = []

    for nome_ruolo, quantita in COMPOSIZIONE_RUOLI.items():
        # Controllo che il ruolo esista davvero in ruoli.json
        if nome_ruolo not in RUOLI_SPECIALI:
            raise ValueError(
                f"'{nome_ruolo}' non esiste in ruoli.json. Controlla il nome (maiuscole/spazi inclusi)."
            )
        lista_ruoli.extend([nome_ruolo] * quantita)

    if len(lista_ruoli) > numero_giocatori:
        raise ValueError(
            f"Hai richiesto {len(lista_ruoli)} ruoli speciali ma ci sono solo {numero_giocatori} giocatori."
        )

    # Riempi i posti rimanenti con Contadini (ruolo base, non serve sia in ruoli.json)
    posti_rimanenti = numero_giocatori - len(lista_ruoli)
    lista_ruoli.extend(["Contadino"] * posti_rimanenti)

    return lista_ruoli


# --- FASE 1: ASSEGNAZIONE CASUALE DEI RUOLI ---
def assegna_ruoli():
    ruoli_da_assegnare = costruisci_lista_ruoli(len(giocatori_connessi))

    # Mescoliamo la lista dei ruoli in modo casuale
    random.shuffle(ruoli_da_assegnare)

    # Associamo ogni giocatore a un ruolo mescolato
    for i in range(len(giocatori_connessi)):
        nome_giocatore = giocatori_connessi[i]
        ruolo_assegnato = ruoli_da_assegnare[i]

        partita[nome_giocatore] = {
            "ruolo": ruolo_assegnato,
            "vivo": True
        }


# --- FASE 2: SCHERMATA DEL NARRATORE (Pannello di Controllo) ---
def mostra_schermata_narratore():
    print("\n--- PANNELLO DEL NARRATORE (Vedi solo tu!) ---")
    for nome, info in partita.items():
        stato = "VIVO" if info["vivo"] else "MORTO"
        ruolo = info["ruolo"]

        # Se è un ruolo speciale, mostriamo anche la fazione presa da ruoli.json
        if ruolo in RUOLI_SPECIALI:
            fazione = RUOLI_SPECIALI[ruolo]["fazione"]
            print(f"Giocatore: {nome} | Ruolo: {ruolo} ({fazione}) | Stato: {stato}")
        else:
            print(f"Giocatore: {nome} | Ruolo: {ruolo} | Stato: {stato}")
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