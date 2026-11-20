# Cycling Suite Common

Librerie condivise da tre applicazioni open source per il ciclismo giovanile, sviluppate per Progetto Ciclismo - Rodengo Saiano A.S.D.:

- **Fuorigiri Performance Lab**: analisi dei test di valutazione, [lucabnt/performance-lab](https://github.com/lucabnt/performance-lab);
- **Ammiraglia** (`club-lab`): gestione della società, repository privata;
- **A Ruota Training Lab** (`training-lab`): programmazione dell'allenamento, repository privata e sviluppo sospeso.

Questa repository non contiene né avvia le applicazioni. Ogni app ha repository, installer, archivi e versioni propri e incorpora una copia versionata delle librerie: non serve un clone di questa repository per compilarle o verificarle. I riferimenti `../club-lab`, `../performance-lab` e `../training-lab` nei documenti indicano checkout affiancati usati dagli script di consegna; per le repository private servono i relativi accessi.

> **In English.** Cycling Suite Common holds the shared libraries (GPL-3.0-or-later) of three youth-cycling applications developed for Progetto Ciclismo - Rodengo Saiano A.S.D., including [Fuorigiri Performance Lab](https://github.com/lucabnt/performance-lab). It contains two packages: `@cycling-suite/ui`, a React 19 + TypeScript component library (theme, responsive shell, fields, tables, dialogs, time inputs, Android-oriented components and fixed club branding) with no network, storage or physiology code; and `cycling-suite-core`, a Python 3.12+ runtime (OS keyring, folder/WebDAV transports, instance lock, Qt window, cryptographic primitives, atomic writes, CSV injection guards, sync jobs and exchange invariants). Data, file formats, access models and sync engines stay in each application. The libraries are not published to a registry: each app vendors a versioned tarball or wheel with recorded checksums, so apps build without this repository. Tags `ui-v*` and `core-v*` mark the delivered versions; the sources of Fuorigiri 0.10.0-alpha.1 are `ui-v0.2.9` and `core-v0.2.0`. To report a vulnerability see [SECURITY.md](SECURITY.md). The rest of the documentation is in Italian.

## Contenuto

| Pacchetto | Versione | Contenuto |
|---|---|---|
| [`@cycling-suite/ui`](packages/ui) | 0.2.9 | React 19 + TypeScript: tema a variabili CSS, shell e navigazione responsive, controlli, Field, liste/tabelle/riepiloghi, Dialog, input dei tempi, componenti Android e branding societario fisso. Nessuna rete, storage o motore fisiologico. |
| [`cycling-suite-core`](packages/core) | 0.2.0 | Runtime Python 3.12+: portachiavi del sistema operativo, trasporti cartella/WebDAV, lock di istanza, finestra Qt, primitive crittografiche, scritture atomiche, CSV sicuro, job di sync e invarianti di scambio. Formati, dati e modelli di accesso restano nelle app. |

Consumatori al 19 novembre 2026: le tre app usano UI 0.2.9; Fuorigiri e Ammiraglia usano core 0.2.0, A Ruota core 0.1.2. [Matrice dei consumatori](docs/INTEGRAZIONE.md#consumatori).

Documentazione: [architettura e confini](docs/ARCHITETTURA.md), [runtime Python](docs/CORE_PYTHON.md), [integrazione nelle app](docs/INTEGRAZIONE.md), [contratti Android](docs/UI_ANDROID.md), [pratiche Android](docs/ANDROID_BEST_PRACTICES.md), [changelog](CHANGELOG.md).

Il codice di origine è estratto da Fuorigiri (commit `e1f01bc`) e poi da Ammiraglia, preservandone la licenza GPL-3.0-or-later.

## Sviluppo

Node.js 22 o successivo, npm e Python 3.12 o successivo per il core. Dal clone di questa repository:

```sh
npm ci
npm test
npm run build
npm run dev
```

I vettori byte per byte di `crypto` richiedono `cryptography` (`python -m pip install cryptography==50.0.2`), altrimenti vengono saltati in locale; in CI `CYCLING_SUITE_REQUIRE_CRYPTO=1` rende obbligatoria la loro esecuzione.

Catalogo: http://127.0.0.1:8782. La prima build compila la libreria; dopo averne modificato i sorgenti ricompilare `npm run build -w @cycling-suite/ui`. Il catalogo usa il pacchetto compilato, come le applicazioni. I suoi dati sono inventati e non vengono salvati.

L’[anteprima Android](http://127.0.0.1:8782/?android) esercita paginazione, filtri, editor e dialoghi annidati, caricamento/errore e superfici immersive con pannello richiamabile. È una verifica web, senza simulare un bridge o un grafico scientifico.

```sh
npm run pack:ui
```

Produce `artifacts/cycling-suite-ui-0.2.9.tgz`, comprensivo di JS, dichiarazioni TypeScript, CSS, logo, sorgenti e licenza. Non pubblica su npm o GitHub. [Uso nelle app e bootstrap Ammiraglia](docs/INTEGRAZIONE.md).

Per derivare automaticamente il pacchetto nelle app, con test, installazione, lockfile e provenienza:

```sh
npm run sync:ui -- --app ../club-lab --app ../performance-lab --app ../training-lab
npm run sync:ui -- --app ../club-lab --app ../performance-lab --app ../training-lab --check
```

I workspaces npm qui organizzano **soltanto le librerie e gli esempi comuni**; le applicazioni rimangono esterne. Non sono necessari submodule Git o collegamenti a un clone fratello in produzione.

## Licenza e branding

Codice GPL-3.0-or-later, testo in [LICENSE](LICENSE).

Logo e marchio © [Progetto Ciclismo - Rodengo Saiano A.S.D.](https://www.asdprogettociclismorodengosaiano.it/), che ne mantiene la titolarità: sono distinti dalla licenza del codice e la GPL non concede diritti sul marchio. Dettagli in [NOTICE.md](NOTICE.md). Il footer non accetta logo, società o attribuzione come impostazioni modificabili; soltanto il nome dell’applicazione è variabile. Le credenziali, gli inviti e i dati degli atleti non appartengono a questa repository.

## Android

[Pratiche Android della suite](docs/ANDROID_BEST_PRACTICES.md): navigazione, persistenza società, elenchi, moduli, accessibilità, contenitore e gate di collaudo. Il catalogo `/?android` è una prova web con dati sintetici: non sostituisce il collaudo di bridge, APK o dispositivo.

## Sicurezza

Le vulnerabilità vanno segnalate in privato: vedere [SECURITY.md](SECURITY.md).
