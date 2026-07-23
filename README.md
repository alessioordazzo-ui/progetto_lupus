# progetto_lupus
Bozza di codici che DOVREBBERO far girare la tanto osannata app




Fase 1: Configurazione dell'Ambiente di Lavoro (Oggi)
[ ] 1. Installa Python: Scaricalo dal sito ufficiale. Ricorda di spuntare "Add Python to PATH" durante l'installazione.

[ ] 2. Installa VS Code: Scaricalo e installalo sul tuo computer.

[ ] 3. Configura VS Code: Apri il programma, vai nella sezione Estensioni (icona a quattro quadratini) e installa l'estensione ufficiale Python di Microsoft.

[ ] 4. Crea la cartella del progetto: Crea una cartella sul desktop chiamata LupusApp e aprila dentro VS Code (File > Open Folder).

[ ] 5. Fai il primo test di funzionamento: Crea un file main.py, incolla il codice di logica che ti ho dato nella risposta precedente, premi il tasto "Play" in alto a destra e verifica che nel terminale appaia il testo senza errori.

Fase 2: Sviluppo della Logica di Gioco "Cieca" (Senza Grafica)
[ ] 6. Amplia le regole del gioco: Modifica il codice Python testuale per aggiungere le regole che desideri (es. cosa succede se il Veggente "interroga" qualcuno, o come il Narratore dichiara la fine della partita se i Lupi sono in parità con i Contadini).

[ ] 7. Testa tutte le eccezioni nel terminale: Assicurati che se il Narratore prova a linciare un giocatore già morto, il programma risponda con un errore e non si blocchi.

Fase 3: Studio Grafico e Interfaccia (La parte Estetica)
[ ] 8. Disegna i bozzetti (Wireframe): Prendi carta e penna (o usa Canva/Figma gratuito) e disegna come dovranno apparire le schermate:

La schermata del Narratore (Lista giocatori con i ruoli scoperti e bottoni per linciare).

La schermata del Giocatore (Schermata d'attesa, schermata "Carta Ruolo" segreta).

[ ] 9. Installa le librerie grafiche: Apri il terminale di VS Code e scrivi pip install kivy mivymd per scaricare gli strumenti grafici.

[ ] 10. Crea la prima interfaccia grafica statica: Sostituisci il vecchio codice testuale creando una finestra Kivy basilare con qualche bottone e scritta, solo per capire come posizionare gli elementi sullo schermo.

Fase 4: Sviluppo del Network Locale (Il "Cervello" della Stanza)
[ ] 11. Studia i Socket Python: Crea due file di test separati sul PC, server_test.py (il Narratore) e client_test.py (il Giocatore). Scrivi il codice minimo per far sì che il client invii la scritta "Mi sono connesso" e il server la riceva.

[ ] 12. Unisci la Logica al Network: Fai in modo che quando il Server (Narratore) decide di avviare la partita, invii tramite rete i ruoli generati casualmente ai rispettivi Client (Giocatori).

Fase 5: Unione dei Pezzi (Il Gioco Vero e Proprio)
[ ] 13. Collega la Grafica alla Rete: Fai in modo che quando il codice di rete riceve il messaggio "Sei un Lupo", l'interfaccia grafica di Kivy si aggiorni mostrando la carta del Lupo.

[ ] 14. Gestisci l'azione del Narratore: Fai in modo che quando il Narratore clicca su "Lincia Marco" nella sua interfaccia, l'app invii un segnale al telefono di Marco per mostrare la schermata "Sei stato eliminato".

[ ] 15. Fase di Debug su PC: Apri 3 o 4 finestre contemporaneamente sul tuo computer (1 Server e 3 Client) e gioca una partita da solo per verificare che i dati passino correttamente da una finestra all'altra.

Fase 6: Esportazione su Smartphone (Il Finale)
[ ] 16. Prepara il codice per il mobile: Adatta le dimensioni dei bottoni e dei testi di Kivy in modo che siano leggibili sullo schermo verticale di un telefono.

[ ] 17. Installa Buildozer (per Android): Buildozer è lo strumento gratuito che trasforma il codice Python in un file .apk per Android. (Nota: richiede Linux o un sistema Mac/Google Colab, ti guiderò io quando sarà il momento perché è la parte più tecnica).

[ ] 18. Genera il file .apk: Avvia la compilazione per generare l'applicazione per Android.

[ ] 19. Installa e Gioca: Trasferisci il file .apk sul tuo telefono tramite cavo USB o mandandotelo su WhatsApp, installalo, connetti i tuoi amici al tuo Hotspot Wi-Fi e date il via alla prima partita di Lupus in Fabula!