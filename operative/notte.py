
# notte.py
# Gestisce la registrazione e la risoluzione delle azioni notturne.

from operative.azioni import esegui_azione


class GestoreNotte:

    AZIONI_SUPPORTATE = (
        "proteggi",
        "scopri_allineamento",
        "uccidi"
    )

    def __init__(self):
        self.azioni = []
        self.risultati_privati = {}
        self.risultati_pubblici = []

    def aggiungi_azione(self, nome_azione, attore, bersaglio):
        """
        Registra una sola azione per giocatore
        durante la stessa notte.
        """

        if not attore.get("alive", False):
            return {
                "successo": False,
                "messaggio": "Il giocatore è morto e non può agire."
            }

        if not bersaglio.get("alive", False):
            return {
                "successo": False,
                "messaggio": "Il bersaglio è morto."
            }

        if nome_azione not in self.AZIONI_SUPPORTATE:
            return {
                "successo": False,
                "messaggio": (
                    f"Azione '{nome_azione}' non ancora supportata."
                )
            }

        for azione in self.azioni:
            if azione["attore"]["name"] == attore["name"]:
                return {
                    "successo": False,
                    "messaggio": (
                        f"{attore['name']} ha già registrato "
                        "un'azione questa notte."
                    )
                }

        self.azioni.append({
            "azione": nome_azione,
            "attore": attore,
            "bersaglio": bersaglio
        })

        return {
            "successo": True,
            "messaggio": (
                f"Azione '{nome_azione}' registrata: "
                f"{attore['name']} -> {bersaglio['name']}"
            )
        }

    def risolvi(self):
        """
        Risolve le azioni nell'ordine:
        1. Protezioni
        2. Investigazioni
        3. Attacchi

        I risultati investigativi vengono conservati
        separatamente dai risultati pubblici.
        """

        self.risultati_privati.clear()
        self.risultati_pubblici.clear()

        for tipo_azione in self.AZIONI_SUPPORTATE:
            for azione in self.azioni:

                if azione["azione"] != tipo_azione:
                    continue

                risultato = esegui_azione(
                    azione["azione"],
                    azione["attore"],
                    azione["bersaglio"]
                )

                if risultato.get("informazione_privata", False):
                    nome_attore = azione["attore"]["name"]

                    self.risultati_privati.setdefault(
                        nome_attore, []
                    ).append(risultato)
                else:
                    self.risultati_pubblici.append(risultato)

        return list(self.risultati_pubblici)

    def ottieni_risultati_privati(self, nome_giocatore):
        """
        Restituisce i risultati investigativi
        associati a uno specifico giocatore.
        """

        return list(
            self.risultati_privati.get(nome_giocatore, [])
        )

    def reset(self):
        """
        Svuota lo stato della notte conclusa.
        """

        self.azioni.clear()
        self.risultati_privati.clear()
        self.risultati_pubblici.clear()
