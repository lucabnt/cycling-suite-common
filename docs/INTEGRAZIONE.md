# Integrare Fuorigiri o Ammiraglia

## Artefatto versionato senza dipendenza dal percorso del collega

1. Nella repository comune: `npm ci`, `npm test`, `npm run build`, `npm run pack:ui`.
2. Copiare il file da artifacts nella cartella `frontend/vendor/` della propria app.
3. Dal frontend dell’app eseguire `npm install ./vendor/cycling-suite-ui-0.1.0.tgz --save-exact`.
4. Versionare tarball e package-lock.json nell’app. Il tarball contiene anche i sorgenti GPL, le dichiarazioni TypeScript, il logo e LICENSE.
5. Registrare in un file di provenienza versione, SHA256 e commit/tag della repository comune. Il tag non va spostato dopo la consegna.

La normale build dell’app usa `npm ci` e non cerca cartelle sul PC dello sviluppatore. Non usare `file:../../cycling-suite-common/packages/ui` nelle release: quel percorso non esiste su CI o sul PC degli altri collaboratori. Durante lo sviluppo locale è possibile collegare una copia di lavoro, ma prima della consegna ripristinare la dipendenza versionata e verificarla.

## Primo uso in Ammiraglia

React 19 + TypeScript. Importare tema/componenti e gli export documentati in packages/ui/README.md. La prima versione non impone sidebar o menu: conservare le voci specifiche di Ammiraglia e seguire il catalogo per campi/tabelle/branding. Non copiare style.css o le pagine di analisi di Fuorigiri come base permanente.

L’app importa `SuiteBranding` con productName="Ammiraglia"; non aggiungere una preferenza per cambiarne società/logo/attribuzione. Le autorizzazioni e gli stati di sync devono provenire dal proprio backend: il pacchetto UI non li implementa né li simula nelle app reali.

## Integrazione iniziale Fuorigiri

Fuorigiri consuma Field, SortableTable, DataTable, SuiteBranding e i CSS del pacchetto. I wrapper compatibili rimangono nei moduli esistenti per non cambiare tutti gli import in una sola volta. Il logo per report PDF rimane anche nel backend di Fuorigiri; l’immagine UI condivisa è lo stesso originale, verificabile per SHA256.

Il motore, gli archivi e la sincronizzazione non vengono spostati nella 0.1.0. Questa estrazione non cambia schema del DB, autenticazione, nomi degli eseguibili o metodi fisiologici.

## Coordinamento dei rilasci

Una modifica comune: correggere qui → test e catalogo → nuova versione → nuovo tarball → aggiornamento e verifica di ogni app. Le app possono restare temporaneamente su versioni diverse; tenere una matrice di quelle collaudate e non dichiarare automaticamente compatibili nuove versioni.

Matrice iniziale: Fuorigiri frontend 0.8 + UI 0.1.0 è il consumatore di prova; Ammiraglia è da integrare e collaudare nella sua repository. La libreria non impone una pubblicazione sincronizzata degli installer.
