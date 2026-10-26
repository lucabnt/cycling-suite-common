# Ammiraglia verso il pilot — valutazione del 25 ottobre 2026

**Seguito operativo autorizzato:** consegnata UI 0.2.8 ad Ammiraglia e Fuorigiri; implementata in Ammiraglia la preferenza locale della società con selezione esplicita quando assente/non disponibile. Preparazione candidato Windows e checklist nel prodotto, esiti nel suo `docs/VALIDAZIONE.md`. Le baseline e le proposte sotto descrivono la valutazione precedente all'intervento; la matrice corrente è in INTEGRAZIONE.md.

## Esito e perimetro

Conviene derivare da Fuorigiri soprattutto il percorso di consegna e collaudo, aggiornare il consumo della UI comune e correggere la riapertura della società. Proposta: pilot iniziale Windows, una società, uno o due operatori dello staff e un solo trasporto qualificato. Android non è un prerequisito proposto per questo primo giro: Ammiraglia non ha il contenitore nativo di Fuorigiri.

Questa è una valutazione, non l'avvio operativo del pilot o un'approvazione all'uso di dati reali. Nessuna modifica applicativa, nuova consegna di pacchetti o compilazione. Restano le condizioni espresse da Ammiraglia in `SECURITY.md`, `NOTICE.md` e nella checklist RC2.

## Baseline osservata

| Area | Fuorigiri | Ammiraglia | Implicazione |
|---|---|---|---|
| Sorgenti | 0.10.0; HEAD `7a084a4`, con ulteriori modifiche locali | 0.1.0; HEAD `c3b25ed`, checkout pulito | Non prendere il checkout Fuorigiri come una release immutabile |
| UI | 0.2.8, allineata alla sorgente common | 0.2.2, integra ma superata | Consegnare esplicitamente la 0.2.8 e collaudare il consumo |
| Core Python | 0.1.2 allineato e installato | 0.1.2 allineato e installato | Nessun aggiornamento core necessario sulla base dei controlli eseguiti |
| Candidato | Consegne pilot Windows/Android e correzioni successive documentate | Portabile Windows RC2 del 21 ottobre, manifest, sorgenti e checklist | Ammiraglia ha già una base concreta di collaudo |
| Qualifica | Checklist e gate esterni ancora aperti | Checklist RC2 con prove operative da svolgere | Il metodo è riusabile; l'accettazione di Fuorigiri non si trasferisce |

Fonti: [matrice dei consumatori](INTEGRAZIONE.md), [revisione precedente](REVISIONE_APPLICAZIONI_2026-10-21.md), `test-analysis/docs/VERIFICA.md`, `club-lab/docs/VALIDAZIONE.md` e `club-lab/docs/COLLAUDO_CANDIDATO_20261021_RC2.md`. I percorsi dei prodotti identificano fonti esterne a questa repository, senza introdurre dipendenze di build.

## Cosa derivare e dove

| Priorità | Intervento | Responsabilità e criterio di completamento |
|---|---|---|
| P0 | Ultima società affidabile | Ammiraglia. In `frontend/src/App.tsx` la preferenza è in localStorage e, se manca/non è valida, viene aperta `entries[0]`. Il desktop sceglie una porta libera a ogni avvio: l'origine del browser può cambiare. Riprendere il criterio di Fuorigiri: preferenza locale del dispositivo tramite backend autenticato, solo ID validati; nessuna apertura automatica di un'altra società se manca quella ricordata. Provare due società, riavvio con porta diversa e ID non più disponibile. Non ripristinare sessioni operatore attraverso questa preferenza. |
| P0 | Allineamento UI | Common possiede già i componenti necessari; aggiornare Ammiraglia tramite `sync:ui`, senza nuove copie o modifiche al vendor. Verificare shell, editor con modifiche, cancel annidato, focus e chiusura durante salvataggio. Una dipendenza aggiornata non prova l'adozione di nuovi layout o componenti. |
| P0 | Candidato congelato e ripetibile | Ammiraglia. Il RC2 ha già checksum/manifest/sorgenti; riprendere da `test-analysis/scripts/package_candidate.py` il metodo per automatizzare la consegna, adattandolo al prodotto. Collegare versione, commit ed eventuali modifiche locali, frontend incluso, dipendenze UI/core, sorgenti e checklist. Nuova destinazione e predecessori conservati. Qualificare il portabile; se il pilot userà il setup, produrre e provare anche quello. |
| P0 | Aggiornamento e recupero | Ammiraglia. Due build distinte, copia QA, backup dati e materiale di recupero accessi abbinato; ripristino su profilo/PC sostitutivo. Conservare UUID, revisioni, gruppi, saldi e continuità delle repliche. La sola esportazione non prova il recupero. |
| P1 | Liste gestibili e ritorno dal dettaglio | Common fornisce già `RecordCards` e filtri. Ammiraglia usa `ListPanel` con tabella completa; lo storico magazzino rende tutti i movimenti e il cambio pagina azzera ricerca/selezione in `App.tsx`. Adottare paginazione e conservazione dello stato dove i volumi del pilot lo richiedono, con filtri e conteggi coerenti. Il recente `SavedReports` di Fuorigiri dimostra il riuso delle schede comuni anche fuori dal caso Android. I modelli delle liste restano applicativi. |
| P1 | Segnali di avanzamento | Adottare gli stati di caricamento comuni per import/export/scambio, dove servono. Il backend determina progresso ed esito; evitare percentuali simulate e messaggi di successo prima della conclusione. |
| P1 | Documentazione corrente | Ammiraglia. `ROADMAP.md` mantiene recupero/rotazione tra i residui M1/M4, mentre implementazione e prove successive sono in `CICLO_ACCESSI_E_CHIAVI.md` e VALIDAZIONE. Distinguere funzioni presenti, qualifica residua e storia; allineare roadmap, perimetro pilot e checklist. |
| P2 | Preferenze dispositivo | Il bootstrap lingua/fuso è in evoluzione locale su Fuorigiri. Valutare soltanto se serve ad Ammiraglia, dopo stabilizzazione; nessuna estrazione immediata in common sulla base di codice non ancora consolidato. |

## Cosa allineare in Common

Il divario dimostrato è nell'adozione della UI, non nella mancanza di una nuova libreria. Per la consegna della 0.2.8 già esistente non occorre inventare una versione successiva. Se emergono difetti e cambiano i byte, incrementare versione UI, catalogo e lockfile prima della nuova consegna.

Aggiornare la matrice in INTEGRAZIONE soltanto dopo consegna e verifiche effettive. Conservare separata l'adozione Android: il consumo della 0.2.8 da Ammiraglia non prova bridge, navigazione nativa o funzionamento APK. Non emergono motivi sufficienti per estendere ora il core con lifecycle server, preferenze, identità o gestione società, che restano applicativi secondo i confini correnti.

Anche la preparazione candidati resta per ora negli script dei prodotti: riusare criteri e struttura senza aggiungere al runtime comune un sistema di release. Un'eventuale estrazione di strumenti di sviluppo richiede due usi stabilizzati e un contratto esplicito.

## Cosa non trasferire automaticamente

- Motori scientifici, zone di allenamento, tracciati, report fisiologici e convenzioni specifiche dei gruppi di Fuorigiri. Ammiraglia ha già gruppi statici/dinamici, periodi e storico KSport propri; verificarli con casi di stagioni passate/future senza sostituirne il modello.
- Sync v2 e backup v3 di Fuorigiri. Ammiraglia conserva journal, firme, cifratura, recupero e formati propri. Nel codice attuale il backup ha limiti di 40.000.000 byte e 100.000 revisioni; lo scambio ha limiti di 20.000 oggetti e 40.000.000 byte. Misurare un corpus rappresentativo prima del pilot. Se insufficiente, progettare una modifica compatibile: alzare i limiti non risolve scalabilità o memoria.
- OAuth Drive/Dropbox/OneDrive e Android. Per il primo pilot sfruttare cartella/WebDAV già implementati; aggiungere provider o piattaforme solo se richiesti dal flusso operativo.
- Invio email effettivo. Mailto e copia assistita restano `not_sent`; nessuna outbox/provider è acquisita per analogia con altri prodotti. Calendari personali in uscita e replica dell'archivio hanno qualifiche separate.
- Condivisione automatica di archivi, persone, UUID o autorizzazioni tra prodotti. L'interoperabilità non deve diventare una dipendenza del pilot gestionale senza un caso d'uso esplicito.

## Sequenza proposta per partire

1. **Definire il giro iniziale:** una società, staff interno, uno o due operatori; persone/tutori, gruppi e storico, scadenze/eventi, KSport, report e backup. Magazzino se effettivamente usato. Trasporto unico per la collaborazione; calendari esterni solo se qualificati separatamente.
2. **Preparare il candidato successore di RC2:** UI aggiornata, selezione società corretta, documentazione coerente, test/build e prova browser; poi bundle, smoke del binario, manifest/checksum/sorgenti e checklist riferita a quel candidato. Per la UI seguire la consegna e le verifiche di entrambe le app previste in AGENTS.md.
3. **Collaudo sintetico con staff:** due sessioni complete su PC pulito; import con anteprima e ripetizione, gruppi/stagioni, rinnovi senza perdita di storico, report, eventuali prestiti/rientri. Su due PC: invito, scambio nei due sensi, conflitto, revoca, rete interrotta, rotazione/rinnovo e recupero. Provare aggiornamento fra build distinte e ripristino.
4. **Passaggio a dati reali:** chiudere i gate già richiesti dal prodotto su revisione indipendente, accessi appropriati, PC/provider e accettazione staff; chiarire chi deve leggere l'intero archivio. Confermare la licenza complessiva e i materiali di distribuzione. Nessuna di queste decisioni risulta presa da questa valutazione.
5. **Pilot limitato:** annotare candidato/digest, operatori, funzioni escluse, anomalie e responsabile dell'esito. Bloccare la promozione per perdita dati, accessi errati, saldi/storici incoerenti o recupero fallito. Correzioni in un nuovo candidato, preservando precedenti e backup.

## Riscontri eseguiti in questa valutazione

- Letti istruzioni, documentazione e sorgenti pertinenti dei tre repository; confrontati cronologia Git e versioni dichiarate. Preservate le modifiche locali di Fuorigiri.
- `node scripts/sync-ui.mjs --app ../test-analysis --check`: riuscito, UI 0.2.8 allineata.
- Controllo UI con entrambe le app: arresto su Ammiraglia, UI superata; coerente con la dipendenza 0.2.2, non prova di tarball corrotto.
- `python scripts/sync-core.py --app ../club-lab --app ../test-analysis --check`: riuscito per entrambe, core 0.1.2 e installazioni verificati.
- Verificatori standalone UI/core di Ammiraglia: riusciti. L'app resta verificabile rispetto ai propri pacchetti senza imporre il clone common.

Non rieseguite suite applicative complete, browser, build o prove su PC/provider reali: non è cambiato il codice. I conteggi e gli smoke dei candidati precedenti rimangono evidenze storiche dei rispettivi registri, non risultati di questa sessione.
