# Decisioni architetturali — UI 0.2.9

## ADR-001: repository esterna e applicazioni autonome

Confermata la preferenza dell’utente: Fuorigiri e Ammiraglia rimangono in repository distinte. Cycling Suite Common ospita soltanto codice e contratti effettivamente condivisibili. Le app dipendono dai pacchetti; la libreria non importa dalle app. Fuorigiri non dipende da Ammiraglia e viceversa.

All’interno di questa sola repository i workspaces npm collegano libreria ed esempio. Non si introduce una monorepo contenente i prodotti. Ogni installer include le dipendenze necessarie: il PC dell’utente non richiede un’installazione separata della libreria né una connessione al repository Git.

## ADR-002: estrazione progressiva

Implementati UI/tokens, campi, tabelle, branding e catalogo. Non si copia l’intero style.css di Fuorigiri: contiene layout applicativo e regole globali stratificate. Si estraggono componenti con un contratto ristretto e CSS esplicito; i fogli legacy vengono ridotti solo dove il componente comune ne assume la responsabilità.

Dalla UI 0.2.2 shell e controlli globali, liste/tabelle/riepiloghi, modali e tempi appartengono alla libreria. `application.css` conserva la cascata più recente di Fuorigiri 0.10.0 e viene importato da entrambe le app; i CSS locali contengono i layout delle pagine e le funzionalità specifiche. `Dialog` usa il dialog nativo per focus, Esc e sfondo inerte, con superficie opaca e testata fissa; `TimeInput` conserva secondi/null e mm:ss. I moduli locali omonimi sono soltanto adattatori di lingua/compatibilità. La libreria non importa traduzioni o modelli delle app. Nome/icona e voci di menu rimangono specifici per app; logo societario e attribuzione sono fissi. Nessun nuovo tema scuro è dichiarato implementato.

## ADR-003: versioni e distribuzione

Pacchetto iniziale 0.1.0, API ancora sperimentale: le versioni 0.x possono richiedere modifiche ai consumatori, sempre documentate. Versioni applicative indipendenti. Per ora release in tarball npm con sorgenti e SHA256, copiato esplicitamente nella directory vendor dell’app: i clone delle app restano compilabili senza repository fratelle. Il pacchetto nasce dalla repository comune, non viene modificato nel vendor.

Pubblicazione su un registro rimandata fino alla scelta dell’organizzazione e dello scope disponibile. Nessun account/namespace npm o repository GitHub è stato registrato da questo codice. Quando si adotta un registro, fissare la versione e aggiornare il lockfile con una PR dedicata. Vietato consumare automaticamente un branch mobile main in una release. CI verifica libreria e catalogo; ogni app verifica anche la propria integrazione.

## ADR-004: dati, client e servizi Python

Il runtime `cycling-suite-core` è disponibile in wheel versionata per portachiavi OS, trasporti immutabili, lock di istanza e finestra Qt: [confini e consegna](CORE_PYTHON.md). API/bridge Android, schemi di prodotto, archivio/revisioni/accessi/backup/sync, motori dei test e pianificazione allenamenti restano nelle app. Le directory client/contracts non vengono presentate come librerie funzionanti.

Condividere una libreria non autorizza a condividere SQLite o chiavi. Archivi locali separati, nessuna migrazione automatica o connessione fra app. Prima dello scambio servono identità stabili, compatibilità degli eventi e record sconosciuti, provenienza, autorizzazioni, regole di conflitto e test incrociati delle versioni. Le liste di tipi ammesse da Fuorigiri oggi non contemplano i record di allenamento.

## ADR-005: convenzioni Android e superfici immersive

UI 0.2.3–0.2.8 centralizza schede paginate, filtri richiudibili, azioni dei moduli, densità mobile, stati di caricamento e superfici grafiche/fullscreen. Gli eventi cancel non attraversano i dialoghi annidati. Il nome accessibile resta presente anche quando il titolo non occupa una fascia visiva; il pannello comandi è richiamabile e chiuso inizialmente. L’ordine del marchio è scelto dal prodotto con variante comune `brand-end`.

Cronologia, ultima società, gesti e motore grafico, priorità del Back, orientamento e barre native sono applicativi. Non si introduce un bridge Android universale o una dipendenza da Plotly nel common. [Contratti](UI_ANDROID.md) e [pratiche Android](ANDROID_BEST_PRACTICES.md); dal 25 ottobre 2026 entrambe le app consumano 0.2.8, senza adozione nativa Android implicita per Ammiraglia. Le prove web del catalogo restano distinte dai gate nativi.


## ADR — blocco condiviso dello scorrimento, 8 novembre 2026

UI 0.2.9 conserva un contatore per documento e lo stile overflow iniziale. Ogni Dialog acquisisce un blocco e lo rilascia una sola volta; solo l’ultimo rilascio ripristina lo stile. Questo evita che il cleanup di una conferma annidata ripristini hidden dopo la chiusura del genitore. Vale anche per ordini di smontaggio diversi, replay degli effetti React e apertura fallita; le app non devono correggere lo stile globalmente.
