# Integrare Fuorigiri o Ammiraglia

## Artefatto versionato senza dipendenza dal percorso del collega

### Procedura automatica

Da questa repository, dopo `npm ci`:

```sh
npm run sync:ui -- --app ../club-lab --app ../test-analysis
npm run sync:ui -- --app ../club-lab --app ../test-analysis --check
```

I percorsi sono argomenti espliciti, non dipendenze dell'app. Il comando esegue test, build e pack della UI; trasferisce il tarball nelle app selezionate; aggiorna dipendenza, installazione e lockfile; registra SHA256, commit e stato del checkout sorgente. Una consegna byte-identica conserva la provenienza originale. `--check` verifica gli artefatti consegnati e richiede che versione e impronta delle sorgenti corrispondano al common corrente. Un vecchio pacchetto coerente ma superato viene rifiutato. Le verifiche standalone delle app verificano invece il pacchetto fissato nel clone, senza un repository fratello. Non effettua commit, push o pubblicazione e non aggiorna automaticamente branch mobili.

Una versione già consegnata con byte diversi viene rifiutata: incrementare la versione UI. Revisionare e versionare nell'app tarball, provenienza, package.json e lockfile; poi eseguire i test/build dell'app. Il trasferimento di più app non è una transazione: su un errore successivo verificare i risultati e ripetere il comando dopo la correzione. I vecchi tarball non vengono cancellati automaticamente.

Se il checkout common è modificato, `source_dirty=true` lo rende esplicito: prima della release produrre l'artefatto da commit/tag stabile. I checksum assicurano coerenza dei byte, non sostituiscono la fiducia nella sorgente o firme di pubblicazione.

### Procedura manuale equivalente

1. Nella repository comune: `npm ci`, `npm test`, `npm run build`, `npm run pack:ui`.
2. Copiare il file da artifacts nella cartella `frontend/vendor/` della propria app.
3. Dal frontend dell’app eseguire `npm install ./vendor/cycling-suite-ui-0.2.8.tgz --save-exact` (versione corrente; verificare `packages/ui/package.json`).
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

Matrice locale verificata il 21 ottobre 2026: Fuorigiri frontend 0.10.0 + UI **0.2.8**, Ammiraglia frontend 0.1.0 + UI **0.2.2**. Le aggiunte Android sono già nel pacchetto fissato da Fuorigiri; non attribuire la stessa adozione ad Ammiraglia. Ogni app conserva i propri test/build. La libreria non impone una pubblicazione sincronizzata degli installer.

Per verificare l’allineamento corrente di Fuorigiri: `npm run sync:ui -- --app ../test-analysis --check`. Il controllo di Ammiraglia rispetto al common corrente segnala intenzionalmente la versione precedente finché non viene eseguita una sua consegna esplicita. Non è un difetto d’integrità del pacchetto 0.2.2.

## Adozione Android

Seguire [pratiche Android](ANDROID_BEST_PRACTICES.md) e [contratti UI](UI_ANDROID.md). La classe `android` è attivata dal prodotto dopo il riconoscimento del contenitore; restringere il browser non deve abilitare API native. Il common non imposta orientamento, persistenza della società, cattura di Back o motore grafico. Il catalogo `/?android` permette di verificare i componenti web separatamente dai gate APK/dispositivo.
