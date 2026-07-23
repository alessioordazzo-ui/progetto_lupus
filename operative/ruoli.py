RUOLI_SPECIALI = {
    # --- FAZIONE UMANI / CONTADINI ---
    "SINDACO": {
        "fazione": "Umani",
        "descrizione": "Il suo voto al rogo vale doppio durante le votazioni di giorno.",
        "tipo": "Guida del Villaggio"
    },
    "MEDICO": {
        "fazione": "Umani",
        "descrizione": "Ogni notte sceglie un giocatore da proteggere. Non può proteggere se stesso due volte di fila.",
        "tipo": "Protettore"
    },
    "VEGGENTE": {
        "fazione": "Umani",
        "descrizione": "Ogni notte indica un giocatore e il Narratore gli rivela se è un Lupo o no.",
        "tipo": "Investigatore"
    },
    "GUARDIA DEL CORPO": {
        "fazione": "Umani",
        "descrizione": "Sceglie un giocatore da proteggere. Se quel giocatore viene attaccato dai Lupi, la Guardia muore al suo posto.",
        "tipo": "Scudo Umano"
    },
    "MITOMANE": {
        "fazione": "Umani (all'inizio)",
        "descrizione": "La seconda notte sceglie un giocatore: ne copia il ruolo per il resto della partita.",
        "tipo": "Cangiante"
    },

    # --- FAZIONE LUPI ---
    "LUPO MITOMANE": {
        "fazione": "Lupi",
        "descrizione": "Agisce come un normale contadino finché non viene attaccato o individuato, poi si sveglia con i Lupi.",
        "tipo": "Infiltrato"
    },
    "LUPO ALCHIMISTA": {
        "fazione": "Lupi",
        "descrizione": "Una volta per partita può silenziare un giocatore per il giorno successivo (non potrà parlare né votare).",
        "tipo": "Lupo Tattico"
    },
    "LUPO SOLITARIO": {
        "fazione": "Lupi",
        "descrizione": "Si sveglia con i Lupi, ma vince SOLO se rimane l'ultimo sopravvissuto di tutta la partita.",
        "tipo": "Traditore"
    },

    # --- MINACCE NEUTRALI / SOLITARI ---
    "PESTILENZA": {
        "fazione": "Solitario",
        "descrizione": "Ogni notte infetta un giocatore. Vince se riesce ad infettare tutti i sopravvissuti.",
        "tipo": "Minaccia Neutrale"
    },
    "BOIA": {
        "fazione": "Solitario",
        "descrizione": "All'inizio della partita gli viene assegnato un bersaglio segreto. Vince se riesce a far linciare quel bersaglio al rogo.",
        "tipo": "Obiettivo Segreto"
    },
    "FLAUTISTA": {
        "fazione": "Solitario",
        "descrizione": "Ogni notte ipnotizza due giocatori. Vince quando tutti i giocatori in vita sono ipnotizzati.",
        "tipo": "Incantatore"
    }
}