# Integrare Fuorigiri o Ammiraglia

## Consegna UI 0.2.9 — 8 novembre 2026

Allineati Fuorigiri, Ammiraglia e A Ruota tramite sync:ui e --check al pacchetto 0.2.9, SHA-256 `b2d93ec844cbf4a399dca37d9bfc6e8a7990320d565886be2d0a262c304b72f4`. Correzione del blocco di scorrimento residuo alla chiusura simultanea di dialoghi annidati. Nessun core Python, dato o formato modificato; nessun nuovo installer/APK o pubblicazione.

Verifiche: common 17 test JavaScript (quattro nuove regressioni sul lock, tutte le sei permutazioni di chiusura di tre finestre), 3 test core Python e build UI/catalogo. Test/build frontend dei consumatori: Fuorigiri 43, Ammiraglia 6, A Ruota 20, tutti passati; controlli standalone UI e allineamento sorgenti/tarball/lock riusciti. Browser compilato Fuorigiri: riprodotto overflow hidden senza finestre prima della correzione; con 0.2.9, annullamento lascia bloccato il genitore, eliminazione libera la pagina e la pagina successiva scorre. Prova web, non Android nativo né collaudo GUI completo delle altre due app.

Le matrici datate precedenti rimangono fotografie storiche delle rispettive consegne.

## Artefatto versionato senza dipendenza dal percorso del collega

### Procedura automatica

Da questa repository, dopo `npm ci`:

```sh
npm run sync:ui -- --app ../club-lab --app ../performance-lab --app ../training-lab
npm run sync:ui -- --app ../club-lab --app ../performance-lab --app ../training-lab --check
```

I percorsi sono argomenti espliciti, non dipendenze dell'app. Il comando esegue test, build e pack della UI; trasferisce il tarball nelle app selezionate; aggiorna dipendenza, installazione e lockfile; registra SHA256, commit e stato del checkout sorgente. Una consegna byte-identica conserva la provenienza originale. `--check` verifica gli artefatti consegnati e richiede che versione e impronta delle sorgenti corrispondano al common corrente. Un vecchio pacchetto coerente ma superato viene rifiutato. Le verifiche standalone delle app verificano invece il pacchetto fissato nel clone, senza un repository fratello. Non effettua commit, push o pubblicazione e non aggiorna automaticamente branch mobili.

Una versione già consegnata con byte diversi viene rifiutata: incrementare la versione UI. Revisionare e versionare nell'app tarball, provenienza, package.json e lockfile; poi eseguire i test/build dell'app. Il trasferimento di più app non è una transazione: su un errore successivo verificare i risultati e ripetere il comando dopo la correzione. I vecchi tarball non vengono cancellati automaticamente.

Se il checkout common è modificato, `source_dirty=true` lo rende esplicito: prima della release produrre l'artefatto da commit/tag stabile. I checksum assicurano coerenza dei byte, non sostituiscono la fiducia nella sorgente o firme di pubblicazione.

### Procedura manuale equivalente

1. Nella repository comune: `npm ci`, `npm test`, `npm run build`, `npm run pack:ui`.
2. Copiare il file da artifacts nella cartella `frontend/vendor/` della propria app.
3. Dal frontend dell’app eseguire `npm install ./vendor/cycling-suite-ui-0.2.9.tgz --save-exact` (versione corrente; verificare `packages/ui/package.json`).
4. Versionare tarball e package-lock.json nell’app. Il tarball contiene anche i sorgenti GPL, le dichiarazioni TypeScript, il logo e LICENSE.
5. Registrare in un file di provenienza versione, SHA256 e commit/tag della repository comune. Il tag non va spostato dopo la consegna.

La normale build dell’app usa `npm ci` e non cerca cartelle sul PC dello sviluppatore. Non usare `file:../../cycling-suite-common/packages/ui` nelle release: quel percorso non esiste su CI o sul PC degli altri collaboratori. Durante lo sviluppo locale è possibile collegare una copia di lavoro, ma prima della consegna ripristinare la dipendenza versionata e verificarla.

## Primo uso in Ammiraglia

React 19 + TypeScript. Importare tema/componenti e gli export documentati in packages/ui/README.md. La versione 0.2.2 fornisce gli stili della shell: importare `theme.css`, `components.css`, `application.css` e infine gli stili delle pagine. Conservare nomi, loghi applicativi e voci specifiche. I wrapper `Modal`/`Dialog` devono delegare al componente comune; evitare copie di componenti, validazione tempi o CSS condivisi. Non copiare style.css o le pagine di analisi di Fuorigiri come base permanente.

L’app importa `SuiteBranding` con productName="Ammiraglia"; non aggiungere una preferenza per cambiarne società/logo/attribuzione. Le autorizzazioni e gli stati di sync devono provenire dal proprio backend: il pacchetto UI non li implementa né li simula nelle app reali.

## Integrazione iniziale Fuorigiri

Fuorigiri consuma Field, SortableTable, DataTable, SuiteBranding e i CSS del pacchetto. I wrapper compatibili rimangono nei moduli esistenti per non cambiare tutti gli import in una sola volta. Il logo per report PDF rimane anche nel backend di Fuorigiri; l’immagine UI condivisa è lo stesso originale, verificabile per SHA256.

Il motore, gli archivi e la sincronizzazione non vengono spostati nella 0.1.0. Questa estrazione non cambia schema del DB, autenticazione, nomi degli eseguibili o metodi fisiologici.

## Coordinamento dei rilasci

Una modifica comune: correggere qui → test e catalogo → nuova versione → nuovo tarball → aggiornamento e verifica di ogni app. Le app possono restare temporaneamente su versioni diverse; tenere una matrice di quelle collaudate e non dichiarare automaticamente compatibili nuove versioni.

Matrice locale aggiornata il 25 ottobre 2026: Fuorigiri frontend 0.10.0 + UI **0.2.8**, Ammiraglia frontend 0.1.0 + UI **0.2.8**. Consegna versionata eseguita per entrambe; test/build frontend riusciti (34 Fuorigiri, 6 Ammiraglia). Ammiraglia non adotta automaticamente layout mobili o un contenitore Android: la presenza del pacchetto non prova la stessa adozione di Fuorigiri. Ogni app conserva i propri test/build. La libreria non impone una pubblicazione sincronizzata degli installer.

Per verificare l’allineamento corrente: `npm run sync:ui -- --app ../club-lab --app ../performance-lab --app ../training-lab --check`. Il precedente disallineamento di Ammiraglia alla 0.2.2 è superato dalla consegna del 25 ottobre; i candidati compilati precedentemente conservano la propria versione UI.

## Adozione Android

Seguire [pratiche Android](ANDROID_BEST_PRACTICES.md) e [contratti UI](UI_ANDROID.md). La classe `android` è attivata dal prodotto dopo il riconoscimento del contenitore; restringere il browser non deve abilitare API native. Il common non imposta orientamento, persistenza della società, cattura di Back o motore grafico. Il catalogo `/?android` permette di verificare i componenti web separatamente dai gate APK/dispositivo.

## Allineamento del 2 novembre 2026

| Consumatore | Repository corrente | UI | Core Python | Verifica |
|---|---|---|---|---|
| Ammiraglia | `club-lab` | 0.2.8 | 0.1.2 | UI sorgenti/tarball/lock e core/installazione verificati |
| Fuorigiri Performance Lab | `performance-lab` (già `test-analysis`) | 0.2.8 | 0.1.2 | UI sorgenti/tarball/lock e core/installazione verificati |
| A Ruota Training Lab | `training-lab` | 0.2.8 | 0.1.2 | UI sorgenti/tarball/lock e core/installazione verificati |

Lockfile con hash (`lock_hashes.py`, 15 novembre 2026): adottati in Fuorigiri (`requirements-lock-windows.hashes`, workflow con `--require-hashes`). Ammiraglia e A Ruota non ancora: alla prossima consegna del core ricevono lo script, poi servono `lock_hashes.py --write` e l'aggiornamento dei loro workflow.

I controlli `sync:ui --check` e `sync-core.py --check` sono riusciti sui tre checkout. Gli artefatti sono già identici alle sorgenti comuni: non serve una nuova versione o consegna. La provenienza originale degli artefatti resta conservata. Questi controlli non qualificano nuovamente installer, APK o dispositivi.

Le ultime modifiche organizzano i comandi contestuali nella testata, seguiti da filtri ed elenco; modello/file e istruzioni estese si aprono su richiesta. Le appartenenze collettive si gestiscono in Gruppi, quelle individuali nel profilo. Questa convenzione vale per la suite, ma layout delle pagine, import CSV, mapping e autorizzazioni restano applicativi. Non richiede spostare i tracciati di prodotto nel common o aggiungere funzioni per uniformare nominalmente i menu.
