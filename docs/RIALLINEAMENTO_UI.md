# Riallineamento UI — 20 ottobre 2026

## Differenze trovate

Le app consumavano UI 0.1.0. Fuorigiri 0.10.0 (`fd569ca`) conservava localmente shell/controlli e stili, correzioni responsive e per superfici opache desktop, Dialog con testata fissa/focus/Esc/conferma di scarto, TimeInput e parsing mm:ss. Ammiraglia aveva una shell simile ma duplicata e una modale nativa distinta, senza conferma delle modifiche. Common conteneva soltanto token, campi, tabelle e branding.

## Risultato

Entrambe dipendono dall'identico `@cycling-suite/ui` 0.2.2, con tarball, checksum, provenienza e lockfile autonomi. Common possiede tema/font, shell/navigazione/controlli responsive, liste/tabelle/riepiloghi e relativi stili; Dialog nativo con sfondo inerte/opaco, focus iniziale e ripristinato, Esc, testata fissa, blocco durante salvataggio e protezione editor; TimeInput/clock/parseClock/validTimes.

Le implementazioni duplicate sono state rimosse: i moduli locali Dialog/Modal/tempi sono adattatori. Ammiraglia applica lo stato vuoto compatto nelle liste. Traduzioni, nomi/loghi prodotto, voci di navigazione, contenuti scientifici e layout delle pagine (pannelli, calendari, grafici, esportazioni) restano specifici. Nessuno spostamento di backend, dati, metodi, autorizzazioni o sincronizzazione.

`sync:ui --check` confronta ora la versione e l'impronta delle sorgenti comuni, oltre all'integrità di artefatto e lockfile: una vecchia versione coerente non passa più per aggiornata. Le verifiche standalone continuano a funzionare senza il clone fratello, e richiedono anche sorgenti/asset dei nuovi componenti. I README e AGENTS delle app stabiliscono che le correzioni condivise si fanno prima in common.

## Verifiche

- Common: 8 test, build TypeScript, catalogo e pacchetto.
- Ammiraglia: 5 test frontend, build TypeScript/Vite e verifica standalone dell'artefatto.
- Fuorigiri: 19 test frontend, build TypeScript/Vite e verifica standalone dell'artefatto.
- Controllo comune finale: entrambe allineate alle sorgenti correnti e stesso tarball.
- Browser su archivi QA nuovi e sintetici: onboarding e shell delle due app; società sintetica, dashboard/liste e scarto protetto in Ammiraglia; finestra licenza in Fuorigiri. Catalogo anche a larghezza ridotta: editor, focus iniziale, Esc con modifiche, ripresa della modifica e chiusura bloccata durante salvataggio.

Il warning Vite relativo al grande bundle Plotly di Fuorigiri resta presente. Non eseguite build installer, prove Qt su PC pulito o collaudi di tutte le pagine con dati complessi. Backend e schemi non modificati; suite backend completa non rieseguita. Nessuna pubblicazione o commit eseguito. Gli artefatti registrano `source_dirty=true`, perché derivano dal lavoro locale ancora da revisionare e committare.

## Aggiornamenti successivi

Modificare common, incrementare la versione del pacchetto e la dipendenza del catalogo, testare e compilare. Consegnare con `npm run sync:ui -- --app ../club-lab --app ../test-analysis`, verificare le due app, quindi eseguire lo stesso comando con `--check`. Import CSS in entrambe: theme, components, application, stili delle pagine. Le app rimangono compilabili senza cartelle sorelle e gli installer esistenti non cambiano da soli.
