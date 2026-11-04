
# notte.py
# Gestione delle azioni notturne e delle indagini.

from operative.azioni import esegui_azione


class GestoreNotte:

    AZIONI_SUPPORTATE = (
        "proteggi",
        "scopri_allineamento",
        "investiga",
        "silenzia",
        "uccidi",
    )

    def __init__(self):
        self.azioni = []
        self.risultati_privati = {}
        self.risultati_pubblici = []

        # Stato persistente delle indagini.
        # Chiave: nome dell'Investigatore.
        self.indagini_in_corso = {}

        self.numero_notte = None

    def imposta_notte(self, numero_notte):
        """
        Imposta il numero della notte corrente.
        """
        self.numero_notte = numero_notte

    def _indagine_pendente(self, nome_attore):
        """
        Recupera un'indagine iniziata esattamente
        nella notte precedente.
        """

        stato = self.indagini_in_corso.get(nome_attore)

        if stato is None or self.numero_notte is None:
            return None

        if self.numero_notte == stato["notte"] + 1:
            return stato

        return None

    def aggiungi_azione(self, nome_azione, attore, bersaglio):
        """
        Registra una sola azione per giocatore
        durante la notte corrente.

        L'Investigatore può scegliere liberamente
        il proprio bersaglio.
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

        if any(
            azione["attore"]["name"] == attore["name"]
            for azione in self.azioni
        ):
            return {
                "successo": False,
                "messaggio": (
                    f"{attore['name']} ha già registrato "
                    "un'azione questa notte."
                )
            }

        if nome_azione == "investiga":
            if self.numero_notte is None:
                return {
                    "successo": False,
                    "messaggio": "Numero della notte non impostato."
                }

        # Nessun vincolo sul bersaglio:
        # cambiarlo è sempre consentito.
        self.azioni.append({
            "azione": nome_azione,
            "attore": attore,
            "bersaglio": bersaglio,
        })

        return {
            "successo": True,
            "messaggio": (
                f"Azione '{nome_azione}' registrata: "
                f"{attore['name']} -> {bersaglio['name']}"
            )
        }

    def _risolvi_indagine(self, attore, bersaglio):
        """
        Se il bersaglio coincide con quello della
        notte precedente, rivela il ruolo esatto.

        Altrimenti rivela la fazione e avvia
        una nuova indagine.
        """

        nome_attore = attore["name"]
        stato = self._indagine_pendente(nome_attore)

        seconda_indagine = (
            stato is not None
            and stato["giocatore"] is bersaglio
            and bersaglio.get("alive", False)
        )

        if seconda_indagine:
            risultato = esegui_azione(
                "investiga_ruolo",
                attore,
                bersaglio
            )

            if risultato.get("successo"):
                # Indagine completata.
                self.indagini_in_corso.pop(
                    nome_attore, None
                )

        else:
            risultato = esegui_azione(
                "investiga_fazione",
                attore,
                bersaglio
            )

            if risultato.get("successo"):
                # Una nuova indagine sostituisce
                # quella precedente.
                self.indagini_in_corso[nome_attore] = {
                    "giocatore": bersaglio,
                    "notte": self.numero_notte,
                }

        return risultato

    def risolvi(self):
        """
        Ordine di risoluzione:
        1. Protezioni
        2. Veggente
        3. Investigatore
        4. Attacchi
        """

        self.risultati_privati.clear()
        self.risultati_pubblici.clear()

        for tipo_azione in self.AZIONI_SUPPORTATE:
            for azione in self.azioni:

                if azione["azione"] != tipo_azione:
                    continue

                attore = azione["attore"]
                bersaglio = azione["bersaglio"]

                if tipo_azione == "investiga":
                    risultato = self._risolvi_indagine(
                        attore,
                        bersaglio
                    )
                else:
                    risultato = esegui_azione(
                        tipo_azione,
                        attore,
                        bersaglio
                    )

                if risultato.get("informazione_privata", False):
                    self.risultati_privati.setdefault(
                        attore["name"], []
                    ).append(risultato)
                else:
                    self.risultati_pubblici.append(risultato)

        return list(self.risultati_pubblici)

    def ottieni_risultati_privati(self, nome_giocatore):
        """
        Restituisce i risultati investigativi
        del giocatore indicato.
        """

        return list(
            self.risultati_privati.get(nome_giocatore, [])
        )

    def reset(self):
        """
        Cancella azioni e risultati della notte.

        Conserva lo stato delle indagini per
        verificare la notte successiva.
        """

        self.azioni.clear()
        self.risultati_privati.clear()
        self.risultati_pubblici.clear()
