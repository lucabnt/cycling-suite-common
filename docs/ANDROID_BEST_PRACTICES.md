# Pratiche Android per le app della suite

Consolidamento aggiornato al **21 ottobre 2026**, confrontato con Fuorigiri `30d0f0a` (TD-98–107). Le pratiche valgono anche per nuove app; non implicano che tutte le app le abbiano già adottate. Le prove di prodotto restano nei rispettivi registri. Fuorigiri usa Kotlin/WebView e Python/Chaquopy; altre app possono scegliere un runtime diverso conservando i medesimi contratti UI. [API, esempi e verifica del common](UI_ANDROID.md).

## Confini e riuso

- Repository, dati, credenziali e build di ciascuna app restano separati. Il common distribuisce componenti versionati, non archivi o autenticazioni.
- Usare Dialog, RecordCards, CollapsibleFilters, FormActions, TimeInput e token del pacchetto UI. Menu, voci, route, formule, payload e decisioni sui campi rimangono nel prodotto. Non duplicare CSS nelle app.
- UI corrente **0.2.8**: variante brand-end; 0.2.7 aggiunge fullscreen e FloatingPanel; 0.2.6 isola cancel nei dialoghi annidati e permette i comandi sotto il grafico; 0.2.5 aggiunge ChartFrame/LoadingState e densità moderata; 0.2.4 introduce la paginazione controllabile; 0.2.3 introduce schede paginate e azioni moduli. Fuorigiri consuma 0.2.8, Ammiraglia resta su 0.2.2 finché non si esegue una consegna esplicita. Mai modificare i byte di una versione già consegnata.
- Distinguere il contenitore Android dal browser stretto: il bridge nativo identifica le funzioni disponibili; la larghezza orienta il layout, non autorizzazioni o accesso ai dati.

## Navigazione e memoria della società

- Testata compatta e menu hamburger per società, sezioni, lingua e Info. Identità e attribuzione societarie fisse; versione/licenza/stato offline in Info, raggiungibile anche senza società.
- Indietro: tastiera gestita dal sistema, poi ultimo dialogo aperto con evento cancel e protezione modifiche, poi cronologia di schermate/profilo, infine uscita alla radice. Fuorigiri mantiene il solo hamburger a sinistra: Indietro è affidato al sistema/gesture, senza freccia duplicata.
- Non riprodurre gli archivi o ripristinare vecchi oggetti dati per tornare indietro: memorizzare identificatori, filtri e posizione di scorrimento. Cronologia limitata, svuotata al cambio società. Non attraversare archivi con permessi diversi mediante Back.
- Conservare l’ultima coppia archivio/società in una preferenza persistente di prodotto (sessionStorage da solo non basta alla morte del processo). Solo identificatori, mai dati degli atleti, token o segreti. Scrivere insieme i due ID.
- Prima di aprire, riconciliare la preferenza con l’inventario locale e i permessi attuali. Se l’archivio è sparito, tornare alla scelta esplicita senza aprire automaticamente un’altra società. Gestire risposte asincrone obsolete e preferenze malformate.

## Elenchi e moduli

- Su telefono usare schede con identità, pochi valori leggibili e unità, accesso esplicito al dettaglio. Evitare tabelle larghe per le operazioni frequenti; le tabelle analitiche possono mantenere scorrimento dedicato.
- Paginare gli elenchi, ripartire dalla prima pagina al cambio filtro e rispettare la selezione effettiva. Ricerca, disponibilità del tracciato e protocollo devono restare filtri espliciti; non mescolare metodi solo per semplificare la UI.
- Filtri richiudibili e conteggio visibile. Non nascondere le informazioni necessarie a capire cosa è stato filtrato.
- Campi essenziali per primi, facoltativi in sezioni richiudibili senza perdere i valori. Nulla di assente diventa zero e nessuna priorità UI cambia i calcoli o gli obblighi di dominio.
- Usare gli originali pulsanti di azione dentro FormActions, senza cloni o submit artificiali che saltino validazioni. Nell’editor Android la barra resta nel viewport con la tastiera. Non duplicare pulsanti che possano salvare due volte.
- Date native, inputMode numeric/decimal dove appropriato; mantenere inserimento di segni/decimali quando il dominio li ammette. TimeInput per mm:ss/secondi, API sempre in secondi. Evitare autofocus che apra inutilmente la tastiera.
- Campo invalido raggiungibile e leggibile, messaggi vicini al contesto; bloccare l’uscita durante un salvataggio. Dopo errore conservare bozza e archivio, mai suggerire reset distruttivi come prima soluzione.

## Contenitore, accessibilità e offline

- Gestire barre, cutout e IME sul contenitore della WebView, non solo sul padding della pagina; verificare che chiusura e azioni non finiscano sotto la tastiera.
- Bersagli tattili almeno 48 dp, etichette accessibili, focus/ordine di tabulazione, TalkBack, contrasto e dimensione testo. Il minimo CSS va verificato sul dispositivo, non equiparato automaticamente a dp su ogni configurazione.
- Conservare l’archivio privato dell’app; file tramite picker/SAF e condivisione del sistema. Mai presumere percorsi desktop o convertire content URI in percorsi locali. Indicare limiti reali del bridge per file grandi.
- Modalità offline completa come obiettivo verificabile; sync è distinta da backup. Credenziali nel meccanismo protetto nativo, OAuth e origini del bridge limitati; non esporre stack o token nelle schermate o nei log operativi.
- Mostrare avanzamento fino al primo rendering utilizzabile. Caricare grafici pesanti quando necessari; misurare avvio, memoria e fluidità con il corpus, non soltanto con l’archivio vuoto.

## Build e prove

- Per dipendenze native verificare ABI, API minima, DT_NEEDED/libpython, integrità wheel/RECORD, pagine 16 KB e caricamento reale. Compilazione e abi3audit non sostituiscono l’import nel runtime effettivo. Riparazioni tracciate con originali/hash, mai downgrade nascosti.
- Dichiarare wheel e manifest fra gli input Gradle: una modifica locale deve invalidare il packaging. Includere frontend e risorse legali/branding correnti.
- Separare: test del modello, build frontend, APK, test strumentali, resa visiva, flussi con dati sintetici, telefono ARM64, account cloud reali e release firmata. Dire esplicitamente quali gate rimangono aperti.
- Provare Indietro da elenco/profilo/test/editor sporco, filtri e paginazione, tastiera aperta, riavvio dopo force-stop e società ricordata mancante. I test non devono pulire gli archivi dell’utente.
- Screenshot reali e aggiornati delle viste toccate, con soli dati sintetici; nessuna simulazione di funzionalità. Conservare provenienza e distinguere emulatore, telefono e desktop.

## Riferimenti

- [Accessibilità Android](https://developer.android.com/guide/topics/ui/accessibility/apps).
- [Build e integrazione della suite](INTEGRAZIONE.md).
- Per la ricetta Fedora, le wheel ABI3 e gli esiti su emulatore consultare le guide Android e VERIFICA della repository Fuorigiri. Le procedure di runtime sono specifiche del prodotto.

## Grafici e avvio: adozione Fuorigiri, 21 ottobre 2026

Separare caricamento motore grafico e primo archivio utilizzabile. Caricare i grafici quando visibili; mostrare stato reale e possibilità di riprovare. Default touch dedicato allo scorrimento pagina, esplorazione esplicita con zoom/pan/ripristino e vista ampia chiusa da Indietro. Offrire dati tabellari paginati con unità e mancanti: una figura Plotly non costituisce da sola un’alternativa accessibile. Non ricostruire valori mancanti.

Testata con società/sezione/ruolo, contesto atleta/data/protocollo nel dettaglio. Ridurre padding e margini prima dei bersagli touch; verificare testo ingrandito, focus, contrasto e movimento ridotto. Avvio nativo e caricamento archivio hanno fasi distinte, senza percentuali inventate e senza includere dati o segreti negli errori.

Riferimenti: [configurazione Plotly](https://plotly.com/javascript/configuration-options/), [accessibilità Android Views](https://developer.android.com/guide/topics/ui/accessibility/views/apps-views).

Scorri pagina è il default anche nella vista ampia. Comandi sotto la figura; un solo Indietro esce dalla modalità esplorazione/zoom prima di chiudere il dialogo. Non propagare cancel dal dialogo figlio al genitore.

### Vista ampia in orizzontale — Fuorigiri TD-105

Usare il bridge nativo per una richiesta temporanea di orientamento, conservando e ripristinando la politica precedente quando la vista chiude, si smonta o la WebView ricarica. Non imporre landscape al resto dell’app e non ruotare il DOM con CSS. La rotazione non deve distruggere test/bozza; ridimensionare la figura al viewport e preservare i limiti degli assi. Back da Esplora esce dal modo senza chiudere né rilasciare l’orientamento; Back/X che chiudono la vista lo ripristinano. Qualificare separatamente telefono, tablet e multiwindow, dove il sistema può ignorare la richiesta. [ActivityInfo Android](https://developer.android.com/reference/android/content/pm/ActivityInfo). Implementazione specifica del contenitore prodotto, nessuna nuova versione UI comune necessaria.

### Grafici immersivi e marchio — Fuorigiri TD-106–107

UI 0.2.7 offre Dialog fullscreen, ChartFrame fullscreen e FloatingPanel: rimuovere la fascia visiva del titolo conservando il nome accessibile, X e comandi richiamabili. Figura a pieno viewport; dati/istruzioni accessibili nel pannello. Il prodotto conserva e ripristina visibilità/behavior delle barre native e orientamento; swipe di sistema per barre transitorie. Back: modo grafico, pannello aperto, vista. Non promettere assenza di caption/cutout in ogni configurazione di sistema. [Immersione Android](https://developer.android.com/develop/ui/views/layout/immersive).

Marchio applicativo sempre orizzontale e icona non compressa; logo societario distinto. Nella **testata Android Fuorigiri** il testo precede l’icona, sul lato destro, come precisato sotto. Bootstrap centrati e sidebar desktop conservano la propria composizione. Consegna esplicita a Fuorigiri, non adozione implicita delle altre app.

Correzione esplicita dell’utente TD-106: nella testata Android Fuorigiri nome/tagline allineati a destra e icona dopo la scritta, sul lato destro. Variante brand-end dalla UI 0.2.8; hamburger resta a sinistra. I bootstrap centrati e la sidebar desktop conservano la propria composizione.
