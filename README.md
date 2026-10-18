# Cycling Suite Common

Repository autonoma delle librerie condivise da **Fuorigiri Performance Lab** e **Ammiraglia**. Le applicazioni conservano repository, installer, database e versioni propri. Questa repository non contiene né avvia le due applicazioni.

## Stato 0.1.0

Primo pacchetto realmente utilizzabile: `@cycling-suite/ui`, React 19 + TypeScript, senza motori fisiologici, rete o accesso al database. Include tema a variabili CSS, Field, DataTable, SortableTable e SuiteBranding con logo societario originale locale. Il catalogo interattivo mostra i due nomi applicativi, filtri, ordinamento, zero e mancanti, stato disabilitato e branding fisso.

Il codice di origine è estratto da Fuorigiri, commit `e1f01bc`, preservandone la licenza GPL-3.0-or-later. Non è ancora un design system completo: shell, navigazione, modali, client e backend sono fasi successive. [Confini e decisioni](docs/ARCHITETTURA.md).

## Sviluppo

Node.js 22 o successivo e npm. Dal clone di questa repository:

```sh
npm ci
npm test
npm run build
npm run dev
```

Catalogo: http://127.0.0.1:8782. La prima build compila la libreria; dopo averne modificato i sorgenti ricompilare `npm run build -w @cycling-suite/ui`. Il catalogo usa il pacchetto compilato, come le applicazioni. I suoi dati sono inventati e non vengono salvati.

```sh
npm run pack:ui
```

Produce `artifacts/cycling-suite-ui-0.1.0.tgz`, comprensivo di JS, dichiarazioni TypeScript, CSS, logo, sorgenti e licenza. Non pubblica su npm o GitHub. [Uso nelle app e bootstrap Ammiraglia](docs/INTEGRAZIONE.md).

Per derivare automaticamente il pacchetto nelle app, con test, installazione, lockfile e provenienza:

```sh
npm run sync:ui -- --app ../club-lab --app ../test-analysis
npm run sync:ui -- --app ../club-lab --app ../test-analysis --check
```

I workspaces npm qui organizzano **soltanto le librerie e gli esempi comuni**; le applicazioni rimangono esterne. Non sono necessari submodule Git o collegamenti a un clone fratello in produzione.

## Licenza e branding

Codice GPL-3.0-or-later, testo in LICENSE. Il marchio della società è distinto dalla licenza del codice: vedere NOTICE.md. Il footer non accetta logo, società o attribuzione come impostazioni modificabili; soltanto il nome dell’applicazione è variabile. Le credenziali, gli inviti e i dati degli atleti non appartengono a questa repository.
