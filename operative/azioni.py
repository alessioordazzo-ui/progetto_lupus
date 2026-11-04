
# azioni.py
# Gestisce le azioni e le interazioni tra i ruoli.

from operative.ruoli import get_ruolo


# ==========================================
# FUNZIONI DI SUPPORTO
# ==========================================

def ottieni_fazione(giocatore):
    """
    Restituisce la fazione del ruolo del giocatore.
    """

    ruolo = get_ruolo(giocatore.get("role", ""))

    if ruolo is None:
        return None

    return ruolo.get("fazione")


def verifica_giocatori_vivi(attore, bersaglio):
    """
    Controlla che attore e bersaglio siano vivi.

    Restituisce None se il controllo è superato,
    altrimenti restituisce un risultato di errore.
    """

    if not attore.get("alive", False):
        return {
            "successo": False,
            "messaggio": f"{attore['name']} è morto e non può agire."
        }

    if not bersaglio.get("alive", False):
        return {
            "successo": False,
            "messaggio": f"{bersaglio['name']} è morto."
        }

    return None


# ==========================================
# AZIONE: PROTEGGI
# ==========================================

def proteggi(attore, bersaglio):
    """
    Protegge un giocatore dagli attacchi dei Lupi
    durante la notte corrente.
    """

    errore = verifica_giocatori_vivi(attore, bersaglio)

    if errore is not None:
        return errore

    bersaglio["protected"] = True

    return {
        "successo": True,
        "azione": "proteggi",
        "attore": attore["name"],
        "bersaglio": bersaglio["name"],
        "messaggio": (
            f"{attore['name']} protegge {bersaglio['name']}."
        )
    }


# ==========================================
# AZIONE: UCCIDI
# ==========================================

def uccidi(attore, bersaglio):
    """
    Gestisce un attacco tenendo conto del ruolo
    dell'attaccante e del bersaglio.
    """

    errore = verifica_giocatori_vivi(attore, bersaglio)

    if errore is not None:
        return errore

    ruolo_bersaglio = bersaglio.get("role", "")
    fazione_attore = ottieni_fazione(attore)

    # Il Serial Killer è immune agli attacchi dei Lupi.
    if (
        ruolo_bersaglio == "Serial Killer"
        and fazione_attore == "Lupi"
    ):
        return {
            "successo": True,
            "azione": "uccidi",
            "attore": attore["name"],
            "bersaglio": bersaglio["name"],
            "ucciso": False,
            "messaggio": (
                f"{bersaglio['name']} sopravvive "
                "grazie alla sua immunità ai Lupi."
            )
        }

    # Il Curatore protegge dagli attacchi dei Lupi.
    if (
        bersaglio.get("protected", False)
        and fazione_attore == "Lupi"
    ):
        return {
            "successo": True,
            "azione": "uccidi",
            "attore": attore["name"],
            "bersaglio": bersaglio["name"],
            "ucciso": False,
            "messaggio": (
                f"{attore['name']} attacca {bersaglio['name']}, "
                "ma il Curatore lo ha protetto."
            )
        }

    # Attacco riuscito.
    bersaglio["alive"] = False

    return {
        "successo": True,
        "azione": "uccidi",
        "attore": attore["name"],
        "bersaglio": bersaglio["name"],
        "ucciso": True,
        "messaggio": (
            f"{attore['name']} attacca {bersaglio['name']}. "
            f"{bersaglio['name']} muore."
        )
    }


# ==========================================
# AZIONE: SCOPRI ALLINEAMENTO (VEGGENTE)
# ==========================================

def scopri_allineamento(attore, bersaglio):
    """
    La Veggente scopre se un giocatore è buono
    o cattivo.

    Umani = buono
    Lupi = cattivo
    Neutrali = cattivo
    """

    errore = verifica_giocatori_vivi(attore, bersaglio)

    if errore is not None:
        return errore

    fazione = ottieni_fazione(bersaglio)

    if fazione is None:
        return {
            "successo": False,
            "messaggio": "Fazione del bersaglio sconosciuta."
        }

    allineamento = (
        "buono" if fazione == "Umani" else "cattivo"
    )

    return {
        "successo": True,
        "azione": "scopri_allineamento",
        "attore": attore["name"],
        "bersaglio": bersaglio["name"],
        "informazione_privata": True,
        "risultato": allineamento,
        "messaggio": (
            f"{bersaglio['name']} risulta {allineamento}."
        )
    }


# ==========================================
# AZIONE: INVESTIGA FAZIONE
# ==========================================

def investiga_fazione(attore, bersaglio):
    """
    Prima indagine dell'Investigatore.

    Restituisce la fazione esatta del bersaglio:
    Umani, Lupi oppure Neutrali.
    """

    errore = verifica_giocatori_vivi(attore, bersaglio)

    if errore is not None:
        return errore

    fazione = ottieni_fazione(bersaglio)

    if fazione is None:
        return {
            "successo": False,
            "messaggio": "Fazione del bersaglio sconosciuta."
        }

    return {
        "successo": True,
        "azione": "investiga",
        "tipo_indagine": "fazione",
        "attore": attore["name"],
        "bersaglio": bersaglio["name"],
        "informazione_privata": True,
        "risultato": fazione,
        "messaggio": (
            f"{bersaglio['name']} appartiene "
            f"alla fazione {fazione}."
        )
    }


# ==========================================
# AZIONE: INVESTIGA RUOLO
# ==========================================

def investiga_ruolo(attore, bersaglio):
    """
    Seconda indagine dell'Investigatore.

    Restituisce il ruolo esatto del bersaglio.
    """

    errore = verifica_giocatori_vivi(attore, bersaglio)

    if errore is not None:
        return errore

    ruolo = bersaglio.get("role")

    if not ruolo:
        return {
            "successo": False,
            "messaggio": "Ruolo del bersaglio sconosciuto."
        }

    return {
        "successo": True,
        "azione": "investiga",
        "tipo_indagine": "ruolo",
        "attore": attore["name"],
        "bersaglio": bersaglio["name"],
        "informazione_privata": True,
        "risultato": ruolo,
        "messaggio": (
            f"Il ruolo esatto di {bersaglio['name']} "
            f"è {ruolo}."
        )
    }


# ==========================================
# AZIONE: SILENZIA (LUPO SILENZIATORE)
# ==========================================

def silenzia(attore, bersaglio):
    """
    Il Lupo Silenziatore impedisce al bersaglio
    di parlare e votare durante il giorno successivo.

    La durata dell'effetto viene gestita
    dal ciclo giorno/notte.
    """

    errore = verifica_giocatori_vivi(attore, bersaglio)

    if errore is not None:
        return errore

    # Impedisce di parlare durante il giorno.
    bersaglio["silenced"] = True

    # Impedisce di partecipare alla votazione.
    bersaglio["can_vote"] = False

    return {
        "successo": True,
        "azione": "silenzia",
        "attore": attore["name"],
        "bersaglio": bersaglio["name"],
        "informazione_privata": True,
        "risultato": "silenziato",
        "messaggio": (
            f"{bersaglio['name']} è stato silenziato "
            "e non potrà parlare né votare "
            "durante il giorno successivo."
        )
    }


# ==========================================
# DISPATCHER DELLE AZIONI
# ==========================================

def esegui_azione(nome_azione, attore, bersaglio):
    """
    Richiama la funzione associata all'azione.
    """

    if nome_azione == "proteggi":
        return proteggi(attore, bersaglio)

    if nome_azione == "uccidi":
        return uccidi(attore, bersaglio)

    if nome_azione == "scopri_allineamento":
        return scopri_allineamento(attore, bersaglio)

    if nome_azione == "investiga_fazione":
        return investiga_fazione(attore, bersaglio)

    if nome_azione == "investiga_ruolo":
        return investiga_ruolo(attore, bersaglio)

    if nome_azione == "silenzia":
        return silenzia(attore, bersaglio)

    return {
        "successo": False,
        "azione": nome_azione,
        "messaggio": (
            f"Azione '{nome_azione}' non ancora implementata."
        )
    }
