# Cycling Suite Common — istruzioni

Revisione sostanziale: 2 novembre 2026.

Common è l'unica fonte di verità delle parti condivise di Fuorigiri (`performance-lab`, già `test-analysis`), Ammiraglia (`club-lab`) e A Ruota (`training-lab`). Le applicazioni mantengono repository, dati e build autonomi.

- Il runtime Python `cycling-suite-core` contiene portachiavi OS, trasporti immutabili, lock di istanza e finestra Qt derivati da Fuorigiri. Dati, firme/accessi, formati di sync, lifecycle server e compatibilità prodotto restano nelle app. [Consegna e confini](docs/CORE_PYTHON.md).
- Per il core incrementare insieme `packages/core/pyproject.toml` e `src/cycling_suite/__init__.py` prima di cambiare una wheel consegnata. Usare `python scripts/sync-core.py --app ../club-lab --app ../performance-lab --app ../training-lab --install`, poi `--check`; niente modifiche manuali al vendor. Verificare i consumatori e la loro installazione autonoma, preservando servizi vault, canali e lock esistenti. `npm test` include i test Python del core.

- Modificare qui token, shell/controlli, liste/tabelle/riepiloghi, Field, Dialog, tempi e branding societario. Non copiare implementazioni o CSS nelle app. Le app conservano adattatori di lingua, nomi/loghi prodotto, menu e layout/funzioni specifici.
- Leggere le istruzioni della repository sorella prima di modificarla; preservare dati e modifiche preesistenti. Non delegare ad agenti senza richiesta esplicita.
- Incrementare la versione di `packages/ui` prima di cambiare i byte di una versione già consegnata; aggiornare la dipendenza del catalogo e il lockfile. Non cambiare le versioni prodotto per il solo aggiornamento della libreria.
- Verificare `npm test`, `npm run build` e il browser per cambiamenti visivi. Aggiornare le app con `npm run sync:ui -- --app ../club-lab --app ../performance-lab --app ../training-lab`; eseguire poi i test/build delle tre app e `npm run sync:ui -- --app ../club-lab --app ../performance-lab --app ../training-lab --check`.
- `--check` richiede versione e impronta sorgenti correnti, oltre a integrità tarball/lockfile. Le verifiche standalone delle app restano indipendenti dal clone common. Non modificare direttamente il vendor.
- Import CSS: tema, componenti, application.css, poi layout specifici. Per i cambi comuni usare nuova versione e consegna esplicita, mai un branch mobile o un percorso a una repository sorella nelle dipendenze.
- Niente dati reali, rete o storage nella UI comune. Preservare GPL, sorgenti e branding societario fisso. Il codice comune non condivide automaticamente archivi, autorizzazioni o chiavi.
- Riferimenti: README.md, docs/ARCHITETTURA.md, docs/INTEGRAZIONE.md e docs/RIALLINEAMENTO_UI.md. Mantenere queste istruzioni aggiornate quando cambiano i confini stabili.

- Per nuove app o modifiche Android leggere [ANDROID_BEST_PRACTICES.md](docs/ANDROID_BEST_PRACTICES.md). Documentare adozione e verifiche nel prodotto; non assumere che una pratica descritta sia già collaudata in tutte le app.

- Android: ChartFrame/LoadingState e densità sono comuni (UI 0.2.6); modi touch, caricamento del motore grafico e contesto restano nel prodotto. Cancel dei dialoghi annidati deve fermarsi al dialogo attivo, senza chiudere il genitore. Fuorigiri usa solo hamburger a sinistra, comandi sotto il grafico e Scorri pagina predefinito; Back esce prima da Esplora/Zoom. Conservare questa politica e i gate reali nella guida Android, senza attribuire automaticamente l’adozione alle altre app.

- UI 0.2.7: Dialog/ChartFrame fullscreen e FloatingPanel per superfici immersive senza fascia di titolo visiva; conservare nome accessibile e chiusura. Il prodotto gestisce orientamento e barre native con ripristino; marchio sempre in riga; Fuorigiri Android in testata usa testo allineato a destra e icona alla sua destra (brand-end, UI 0.2.8).

- Mantenere [contratti Android e matrice di adozione](docs/UI_ANDROID.md) e catalogo `/?android` coerenti con la guida canonica; verificare paginazione controllata, cancel annidato e superfici immersive. Il catalogo è una prova web con dati sintetici: non equivale a collaudo del bridge, APK, IME o telefono. Aggiornare separatamente la matrice dei consumatori in INTEGRAZIONE.md; una libreria disponibile non prova l’adozione nel prodotto.

- Convenzione delle schede: comandi contestuali in testata, filtri ed elenco dopo; modello/file/istruzioni estese su richiesta. Appartenenze collettive in Gruppi, individuali nel profilo. Componenti e stili condivisi restano nel common; flussi, tracciati CSV e layout specifici restano nelle app. Non introdurre funzioni per una parità nominale.
