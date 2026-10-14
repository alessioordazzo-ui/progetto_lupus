
# azioni.py
# Gestisce le azioni e le interazioni tra i ruoli.

from operative.ruoli import get_ruolo


# =========================
# FUNZIONI DI SUPPORTO
# =========================

def ottieni_fazione(giocatore):
    """
    Restituisce la fazione del ruolo del giocatore.
    """

    ruolo = get_ruolo(giocatore.get("role", ""))

    if ruolo is None:
        return None

    return ruolo.get("fazione")


# =========================
# AZIONE: PROTEGGI
# =========================

def proteggi(attore, bersaglio):
    """
    Protegge un giocatore dagli attacchi dei Lupi
    durante la notte corrente.
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


# =========================
# AZIONE: UCCIDI
# =========================

def uccidi(attore, bersaglio):
    """
    Gestisce un attacco tenendo conto del ruolo
    dell'attaccante e del bersaglio.
    """

    if not attore.get("alive", False):
        return {
            "successo": False,
            "messaggio": f"{attore['name']} è morto e non può agire."
        }

    if not bersaglio.get("alive", False):
        return {
            "successo": False,
            "messaggio": f"{bersaglio['name']} è già morto."
        }

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


# =========================
# AZIONE: SCOPRI ALLINEAMENTO
# =========================

def scopri_allineamento(attore, bersaglio):
    """
    La Veggente scopre se un giocatore è buono
    o cattivo.

    Umani = buono
    Lupi = cattivo
    Neutrali = cattivo
    """

    if not attore.get("alive", False):
        return {
            "successo": False,
            "messaggio": (
                f"{attore['name']} è morto e non può agire."
            )
        }

    if not bersaglio.get("alive", False):
        return {
            "successo": False,
            "messaggio": (
                f"{bersaglio['name']} è morto."
            )
        }

    fazione = ottieni_fazione(bersaglio)

    if fazione is None:
        return {
            "successo": False,
            "messaggio": (
                "Fazione del bersaglio sconosciuta."
            )
        }

    if fazione == "Umani":
        allineamento = "buono"
    else:
        allineamento = "cattivo"

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


# =========================
# DISPATCHER DELLE AZIONI
# =========================

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

    return {
        "successo": False,
        "azione": nome_azione,
        "messaggio": (
            f"Azione '{nome_azione}' non ancora implementata."
        )
    }
