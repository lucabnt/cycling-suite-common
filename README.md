# Cycling Suite Common

Repository autonoma delle librerie condivise da **Fuorigiri Performance Lab** e **Ammiraglia**. Le applicazioni conservano repository, installer, database e versioni propri. Questa repository non contiene né avvia le due applicazioni.

## Stato UI 0.2.8

Disponibile anche **`cycling-suite-core` 0.1.2**: portachiavi OS, trasporti cartella/WebDAV, lock di istanza e finestra desktop derivati da Fuorigiri e consumati dalle due app tramite wheel locale versionata. [Confini, consegna automatica e verifiche](docs/CORE_PYTHON.md). Non condivide dati o autorizzazioni e non rende interoperabili gli archivi.

Pacchetto condiviso: `@cycling-suite/ui`, React 19 + TypeScript, senza motori fisiologici, rete o accesso al database. Include tema a variabili CSS, Field, DataTable, SortableTable e SuiteBranding con logo societario originale locale. Il catalogo interattivo mostra i due nomi applicativi, filtri, ordinamento, zero e mancanti, stato disabilitato e branding fisso.

Il codice di origine è estratto da Fuorigiri, commit `e1f01bc`, e riallineato alla UI 0.10.0 del commit `fd569ca`, preservandone la licenza GPL-3.0-or-later. La UI 0.2.2 centralizza anche shell/navigazione responsive, controlli, liste/tabelle/riepiloghi, finestre native con testata fissa e protezione delle modifiche, input tempi e validazione. Client e backend restano nelle applicazioni. [Confini e decisioni](docs/ARCHITETTURA.md).

La UI **0.2.8**, già consumata da Fuorigiri, comprende inoltre schede paginate con pagina controllabile, filtri richiudibili, azioni dei moduli, densità e controlli Android, caricamento accessibile, contenitori grafici, dialoghi fullscreen e pannelli flottanti. La variante `brand-end` permette nome/tagline a destra e icona dopo il testo. Le convenzioni recepiscono Fuorigiri TD-98–107; bridge, navigazione, gesti, orientamento e barre native restano applicativi. [Contratti ed esempi Android](docs/UI_ANDROID.md), [pratiche della suite](docs/ANDROID_BEST_PRACTICES.md).

## Sviluppo

Node.js 22 o successivo, npm e Python 3.12 o successivo per il core. Dal clone di questa repository:

```sh
npm ci
npm test
npm run build
npm run dev
```

Catalogo: http://127.0.0.1:8782. La prima build compila la libreria; dopo averne modificato i sorgenti ricompilare `npm run build -w @cycling-suite/ui`. Il catalogo usa il pacchetto compilato, come le applicazioni. I suoi dati sono inventati e non vengono salvati.

L’[anteprima Android](http://127.0.0.1:8782/?android) esercita paginazione, filtri, editor e dialoghi annidati, caricamento/errore e superfici immersive con pannello richiamabile. È una verifica web, senza simulare un bridge o un grafico scientifico.

```sh
npm run pack:ui
```

Produce `artifacts/cycling-suite-ui-0.2.8.tgz`, comprensivo di JS, dichiarazioni TypeScript, CSS, logo, sorgenti e licenza. Non pubblica su npm o GitHub. [Uso nelle app e bootstrap Ammiraglia](docs/INTEGRAZIONE.md).

Per derivare automaticamente il pacchetto nelle app, con test, installazione, lockfile e provenienza:

```sh
npm run sync:ui -- --app ../club-lab --app ../test-analysis
npm run sync:ui -- --app ../club-lab --app ../test-analysis --check
```

I workspaces npm qui organizzano **soltanto le librerie e gli esempi comuni**; le applicazioni rimangono esterne. Non sono necessari submodule Git o collegamenti a un clone fratello in produzione.

## Licenza e branding

Codice GPL-3.0-or-later, testo in LICENSE. Il marchio della società è distinto dalla licenza del codice: vedere NOTICE.md. Il footer non accetta logo, società o attribuzione come impostazioni modificabili; soltanto il nome dell’applicazione è variabile. Le credenziali, gli inviti e i dati degli atleti non appartengono a questa repository.

## Android

[Pratiche Android della suite](docs/ANDROID_BEST_PRACTICES.md): navigazione, persistenza società, elenchi, moduli, accessibilità, contenitore e gate di collaudo.
