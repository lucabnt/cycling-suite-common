# Integrare Fuorigiri, Ammiraglia e A Ruota

## Consumatori

| App | Repository | UI | Core Python |
|---|---|---|---|
| Fuorigiri Performance Lab | [`performance-lab`](https://github.com/lucabnt/performance-lab) | 0.2.9 | 0.2.0 |
| Ammiraglia | `club-lab` (privata) | 0.2.9 | 0.2.0 |
| A Ruota Training Lab | `training-lab` (privata, sospesa) | 0.2.9 | 0.1.2 |

Le app possono restare temporaneamente su versioni diverse: ogni app tiene la propria matrice delle versioni collaudate e non dichiara automaticamente compatibili quelle nuove. Le verifiche `--check` provano l'allineamento dei byte, non qualificano nuovamente installer, APK o dispositivi.

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

Il runtime Python segue una procedura analoga con `scripts/sync-core.py`: [consegna del core](CORE_PYTHON.md#consegna-riproducibile).

### Procedura manuale equivalente

1. Nella repository comune: `npm ci`, `npm test`, `npm run build`, `npm run pack:ui`.
2. Copiare il file da artifacts nella cartella `frontend/vendor/` della propria app.
3. Dal frontend dell’app eseguire `npm install ./vendor/cycling-suite-ui-0.2.9.tgz --save-exact` (versione corrente; verificare `packages/ui/package.json`).
4. Versionare tarball e package-lock.json nell’app. Il tarball contiene anche i sorgenti GPL, le dichiarazioni TypeScript, il logo e LICENSE.
5. Registrare in un file di provenienza versione, SHA256 e commit/tag della repository comune. Il tag non va spostato dopo la consegna.

La normale build dell’app usa `npm ci` e non cerca cartelle sul PC dello sviluppatore. Non usare `file:../../cycling-suite-common/packages/ui` nelle release: quel percorso non esiste su CI o sul PC degli altri collaboratori. Durante lo sviluppo locale è possibile collegare una copia di lavoro, ma prima della consegna ripristinare la dipendenza versionata e verificarla.

## Uso nelle app

React 19 + TypeScript. Importare tema/componenti e gli export documentati in [packages/ui/README.md](../packages/ui/README.md): `theme.css`, `components.css`, `application.css` e infine gli stili delle pagine. Conservare nomi, loghi applicativi e voci specifiche. I wrapper locali `Modal`/`Dialog` devono delegare al componente comune; evitare copie di componenti, validazione tempi o CSS condivisi.

Ogni app importa `SuiteBranding` con il proprio `productName`; non aggiungere una preferenza per cambiarne società, logo o attribuzione. Autorizzazioni e stati di sync provengono dal backend dell'app: il pacchetto UI non li implementa né li simula.

Motore, archivi e sincronizzazione restano nelle app. L'adozione della libreria non cambia schema del DB, autenticazione, nomi degli eseguibili o metodi fisiologici.

## Coordinamento dei rilasci

Una modifica comune: correggere qui → test e catalogo → nuova versione → nuovo tarball → aggiornamento e verifica di ogni app. La libreria non impone una pubblicazione sincronizzata degli installer.

Convenzione delle schede: comandi contestuali in testata, filtri ed elenco dopo; modello/file e istruzioni estese su richiesta. Appartenenze collettive in Gruppi, individuali nel profilo. Layout delle pagine, import CSV, mapping e autorizzazioni restano applicativi; non si aggiungono funzioni per uniformare nominalmente i menu.

## Adozione Android

Seguire [pratiche Android](ANDROID_BEST_PRACTICES.md) e [contratti UI](UI_ANDROID.md). La classe `android` è attivata dal prodotto dopo il riconoscimento del contenitore; restringere il browser non deve abilitare API native. Il common non imposta orientamento, persistenza della società, cattura di Back o motore grafico. Il catalogo `/?android` permette di verificare i componenti web separatamente dai gate APK/dispositivo. La presenza del pacchetto in un'app non prova l'adozione Android: oggi solo Fuorigiri ha un contenitore Android.
