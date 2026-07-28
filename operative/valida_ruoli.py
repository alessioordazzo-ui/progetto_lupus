# valida_ruoli.py
# Lancia questo script da terminale ogni volta che modifichi ruoli.json,
# PRIMA di aprire l'app. Controlla errori di sintassi e di contenuto
# e ti dice esattamente cosa correggere.
#
# Uso:  python valida_ruoli.py 

import json
import os
import sys

_CARTELLA_CORRENTE = os.path.dirname(os.path.abspath(__file__))
_PERCORSO_JSON = os.path.join(_CARTELLA_CORRENTE, "ruoli.json")

CAMPI_OBBLIGATORI = {"fazione", "tipo", "descrizione"}
FAZIONI_VALIDE = {"Umani", "Lupi", "Neutrale"}


def valida():
    errori = []
    avvisi = []

    # 1. Il file esiste?
    if not os.path.exists(_PERCORSO_JSON):
        print(f"❌ ERRORE: non trovo il file '{_PERCORSO_JSON}'.")
        return False

    # 2. È JSON valido?
    with open(_PERCORSO_JSON, "r", encoding="utf-8") as f:
        contenuto_grezzo = f.read()

    try:
        dati = json.loads(contenuto_grezzo)
    except json.JSONDecodeError as e:
        print(f"❌ ERRORE DI SINTASSI JSON: {e}")
        print("   Controlla virgole, virgolette o parentesi graffe mancanti/in eccesso.")
        return False

    # 3. Deve essere un dizionario (oggetto), non una lista
    if not isinstance(dati, dict):
        print("❌ ERRORE: il file deve contenere un oggetto { ... }, non una lista [ ... ].")
        return False

    if len(dati) == 0:
        avvisi.append("Il file ruoli.json è vuoto: nessun ruolo definito.")

    # 4. Controllo di ogni ruolo
    for nome_ruolo, info in dati.items():

        if not isinstance(info, dict):
            errori.append(f"'{nome_ruolo}': deve essere un oggetto {{...}} con fazione/tipo/descrizione.")
            continue

        campi_presenti = set(info.keys())

        # Campi mancanti
        mancanti = CAMPI_OBBLIGATORI - campi_presenti
        if mancanti:
            errori.append(f"'{nome_ruolo}': mancano i campi {sorted(mancanti)}.")

        # Campi extra non previsti (solo avviso, non blocca)
        extra = campi_presenti - CAMPI_OBBLIGATORI
        if extra:
            avvisi.append(f"'{nome_ruolo}': ha campi extra non usati dal codice {sorted(extra)}.")

        # Valori vuoti
        for campo in CAMPI_OBBLIGATORI & campi_presenti:
            valore = info[campo]
            if not isinstance(valore, str):
                errori.append(f"'{nome_ruolo}': il campo '{campo}' deve essere testo, trovato {type(valore).__name__}.")
            elif valore.strip() == "":
                errori.append(f"'{nome_ruolo}': il campo '{campo}' è vuoto.")

        # Fazione valida (avviso, non blocca: magari stai per aggiungerne una nuova)
        if "fazione" in info and isinstance(info["fazione"], str):
            if info["fazione"] not in FAZIONI_VALIDE:
                avvisi.append(
                    f"'{nome_ruolo}': fazione '{info['fazione']}' non è tra quelle standard "
                    f"{sorted(FAZIONI_VALIDE)}. Se è voluto (nuova fazione), ignora questo avviso."
                )

    # --- Riepilogo ---
    print(f"Ruoli trovati: {len(dati)}")

    if avvisi:
        print(f"\n⚠️  {len(avvisi)} avviso/i (non bloccanti):")
        for a in avvisi:
            print(f"   - {a}")

    if errori:
        print(f"\n❌ {len(errori)} errore/i da correggere:")
        for e in errori:
            print(f"   - {e}")
        print("\nRisultato: NON VALIDO. Correggi ruoli.json prima di avviare l'app.")
        return False

    print("\n✅ Tutto ok: ruoli.json è valido e pronto all'uso.")
    return True


if __name__ == "__main__":
    ok = valida()
    sys.exit(0 if ok else 1)