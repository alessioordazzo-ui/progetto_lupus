
# notte.py
# Gestisce la registrazione e la risoluzione delle azioni notturne.

from operative.azioni import esegui_azione


class GestoreNotte:

    def __init__(self):
        self.azioni = []

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

        # Controlla se il giocatore ha già agito
        for azione in self.azioni:
            if azione["attore"]["name"] == attore["name"]:
                return {
                    "successo": False,
                    "messaggio": (
                        f"{attore['name']} ha già registrato "
                        "un'azione questa notte."
                    )
                }

        if nome_azione not in ("proteggi", "uccidi"):
            return {
                "successo": False,
                "messaggio": (
                    f"Azione '{nome_azione}' non ancora supportata."
                )
            }

        azione = {
            "azione": nome_azione,
            "attore": attore,
            "bersaglio": bersaglio
        }

        self.azioni.append(azione)

        return {
            "successo": True,
            "messaggio": (
                f"Azione '{nome_azione}' registrata: "
                f"{attore['name']} -> {bersaglio['name']}"
            )
        }

    def risolvi(self):
        """
        Risolve le azioni in ordine di priorità:
        prima protezioni, poi attacchi.
        """

        risultati = []

        for tipo_azione in ("proteggi", "uccidi"):
            for azione in self.azioni:

                if azione["azione"] != tipo_azione:
                    continue

                risultato = esegui_azione(
                    azione["azione"],
                    azione["attore"],
                    azione["bersaglio"]
                )

                risultati.append(risultato)

        return risultati

    def reset(self):
        """
        Svuota tutte le azioni della notte.
        """
        self.azioni.clear()
