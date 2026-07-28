# ruoli.py
# Carica il database dei ruoli speciali da ruoli.json.
# Per aggiungere/rimuovere/modificare un personaggio basta editare
# il file ruoli.json: non serve toccare questo codice.

import json
import os

# Percorso assoluto: così funziona indipendentemente da dove lanci lo script
_CARTELLA_CORRENTE = os.path.dirname(os.path.abspath(__file__))
_PERCORSO_JSON = os.path.join(_CARTELLA_CORRENTE, "ruoli.json")


def _carica_ruoli(percorso=_PERCORSO_JSON):
    """Legge il file JSON e ritorna il dizionario dei ruoli.
    Valida che ogni ruolo abbia i campi obbligatori."""
    try:
        with open(percorso, "r", encoding="utf-8") as f:
            dati = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Non trovo '{percorso}'. Assicurati che ruoli.json sia nella stessa cartella di ruoli.py."
        )
    except json.JSONDecodeError as e:
        raise ValueError(f"ruoli.json contiene un errore di sintassi JSON: {e}")

    campi_obbligatori = {"fazione", "tipo", "descrizione"}
    for nome, info in dati.items():
        mancanti = campi_obbligatori - info.keys()
        if mancanti:
            raise ValueError(f"Il ruolo '{nome}' in ruoli.json non ha i campi: {mancanti}")

    return dati


# Caricato una sola volta all'importazione del modulo
RUOLI_SPECIALI = _carica_ruoli()


def ricarica_ruoli():
    """Ricarica ruoli.json da disco (utile se lo modifichi mentre l'app è aperta,
    es. da una futura schermata 'Gestione Ruoli' in Kivy)."""
    global RUOLI_SPECIALI
    RUOLI_SPECIALI = _carica_ruoli()
    return RUOLI_SPECIALI


def get_ruoli_per_fazione(fazione):
    """Ritorna un dizionario con solo i ruoli appartenenti alla fazione indicata."""
    return {nome: dati for nome, dati in RUOLI_SPECIALI.items() if dati["fazione"] == fazione}


def get_nomi_ruoli():
    """Ritorna la lista dei nomi di tutti i ruoli disponibili."""
    return list(RUOLI_SPECIALI.keys())


def descrivi_ruolo(nome_ruolo):
    """Ritorna una stringa leggibile con le info di un ruolo, o un messaggio di errore se non esiste."""
    ruolo = RUOLI_SPECIALI.get(nome_ruolo)
    if not ruolo:
        return f"Ruolo '{nome_ruolo}' non trovato."
    return (f"{nome_ruolo} [{ruolo['fazione']}] - {ruolo['tipo']}\n"
            f"  {ruolo['descrizione']}")


if __name__ == "__main__":
    # Piccolo self-test manuale: stampa tutti i ruoli raggruppati per fazione
    for fazione in ("Umani", "Lupi", "Neutrale"):
        print(f"\n=== {fazione.upper()} ===")
        for nome in get_ruoli_per_fazione(fazione):
            print(descrivi_ruolo(nome))