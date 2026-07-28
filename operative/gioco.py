# gioco.py
# Tutta la logica della partita vive qui, senza nessuna dipendenza da
# terminale o interfaccia grafica. Sia il test da terminale sia la GUI
# Kivy chiamano queste stesse funzioni: quando arriverà la rete (Fase 4),
# saranno queste le funzioni che generano i dati da mandare via socket.

import random
from ruoli import RUOLI_SPECIALI  # legge i dati da ruoli.json

# --- CONFIGURAZIONE PARTITA ---

# Quanti ruoli speciali vuoi in partita. I nomi devono esistere in ruoli.json.
# Tutti i posti non coperti diventano automaticamente "Contadino".
COMPOSIZIONE_RUOLI = {
    "Veggente": 1,
    "Medico": 1,
    "Lupo Silenziatore": 2,
}

# Lista dei giocatori connessi alla stanza
giocatori_connessi = ["Alice", "Bob", "Carlo", "Diana", "Elena", "Fabio", "Giorgio"]

# Dizionario che contiene la partita: { "NomeGiocatore": {"ruolo": "...", "vivo": True} }
partita = {}


# --- ASSEGNAZIONE RUOLI ---

def costruisci_lista_ruoli(numero_giocatori):
    """Costruisce la lista dei ruoli da assegnare, partendo da COMPOSIZIONE_RUOLI
    e riempiendo i posti restanti con 'Contadino'."""

    lista_ruoli = []

    for nome_ruolo, quantita in COMPOSIZIONE_RUOLI.items():
        if nome_ruolo not in RUOLI_SPECIALI:
            raise ValueError(
                f"'{nome_ruolo}' non esiste in ruoli.json. Controlla il nome (maiuscole/spazi inclusi)."
            )
        lista_ruoli.extend([nome_ruolo] * quantita)

    if len(lista_ruoli) > numero_giocatori:
        raise ValueError(
            f"Hai richiesto {len(lista_ruoli)} ruoli speciali ma ci sono solo {numero_giocatori} giocatori."
        )

    posti_rimanenti = numero_giocatori - len(lista_ruoli)
    lista_ruoli.extend(["Contadino"] * posti_rimanenti)

    return lista_ruoli


def assegna_ruoli():
    """Mescola e assegna un ruolo a ogni giocatore connesso. Da chiamare una volta
    all'inizio della partita (sia in terminale che all'avvio della GUI)."""
    ruoli_da_assegnare = costruisci_lista_ruoli(len(giocatori_connessi))
    random.shuffle(ruoli_da_assegnare)

    for i, nome_giocatore in enumerate(giocatori_connessi):
        partita[nome_giocatore] = {
            "ruolo": ruoli_da_assegnare[i],
            "vivo": True,
        }


# --- HELPER: FAZIONE DI UN RUOLO ---

def fazione_di(nome_ruolo):
    """Ritorna la fazione di un ruolo, sia esso speciale (da ruoli.json) o Contadino."""
    if nome_ruolo == "Contadino":
        return "Umani"
    if nome_ruolo in RUOLI_SPECIALI:
        return RUOLI_SPECIALI[nome_ruolo]["fazione"]
    return "Sconosciuta"


# --- AZIONI DEL NARRATORE ---

def lincia_giocatore(nome_bersaglio):
    """Elimina un giocatore. Ritorna (successo: bool, messaggio: str) così la GUI
    può mostrare il messaggio senza dover leggere dal terminale."""
    if nome_bersaglio not in partita:
        return False, "Giocatore non trovato nella stanza."

    info = partita[nome_bersaglio]
    if not info["vivo"]:
        return False, f"{nome_bersaglio} è già morto."

    info["vivo"] = False
    messaggio = f"💥 Il Narratore ha eliminato {nome_bersaglio}! Era un {info['ruolo']}."
    print(messaggio)
    return True, messaggio


# --- VISTA NARRATORE ---
# Il Narratore vede TUTTO: nome, ruolo, fazione e stato di ogni giocatore.

def vista_narratore():
    """Ritorna una lista di dizionari, uno per giocatore, con tutte le info
    che solo il Narratore deve vedere."""
    vista = []
    for nome, info in partita.items():
        vista.append({
            "nome": nome,
            "ruolo": info["ruolo"],
            "fazione": fazione_di(info["ruolo"]),
            "vivo": info["vivo"],
        })
    return vista


def mostra_schermata_narratore():
    """Versione da terminale della vista Narratore (utile per test rapidi)."""
    print("\n--- PANNELLO DEL NARRATORE (Vedi solo tu!) ---")
    for riga in vista_narratore():
        stato = "VIVO" if riga["vivo"] else "MORTO"
        print(f"Giocatore: {riga['nome']} | Ruolo: {riga['ruolo']} ({riga['fazione']}) | Stato: {stato}")
    print("---------------------------------------------\n")


# --- VISTA GIOCATORE ---
# Ogni giocatore vede SOLO il proprio ruolo. Se appartiene alla fazione Lupi,
# vede anche chi sono gli altri lupi (compagni di squadra), come da regole del gioco.

def vista_giocatore(nome_giocatore):
    """Ritorna cosa deve vedere UN SOLO giocatore: il proprio ruolo, la fazione,
    la descrizione, e — solo se è un Lupo — la lista dei suoi compagni Lupi."""
    if nome_giocatore not in partita:
        raise ValueError(f"Giocatore '{nome_giocatore}' non trovato in partita.")

    info = partita[nome_giocatore]
    ruolo = info["ruolo"]
    fazione = fazione_di(ruolo)

    if ruolo in RUOLI_SPECIALI:
        descrizione = RUOLI_SPECIALI[ruolo]["descrizione"]
    else:
        descrizione = "Non hai poteri speciali: usa il buon senso e la parola durante il giorno."

    dati_vista = {
        "nome": nome_giocatore,
        "ruolo": ruolo,
        "fazione": fazione,
        "descrizione": descrizione,
        "vivo": info["vivo"],
        "altri_lupi": None,  # resta None per tutti tranne che per i Lupi
    }

    if fazione == "Lupi":
        dati_vista["altri_lupi"] = [
            {"nome": altro_nome, "vivo": altro_info["vivo"]}
            for altro_nome, altro_info in partita.items()
            if altro_nome != nome_giocatore and fazione_di(altro_info["ruolo"]) == "Lupi"
        ]

    return dati_vista