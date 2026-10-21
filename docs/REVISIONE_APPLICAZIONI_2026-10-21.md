# Revisione di Ammiraglia e Fuorigiri — 21 ottobre 2026

**Aggiornamento successivo richiesto dall'utente:** ricompilazione delle correzioni nei candidati Ammiraglia `20261021-rc2` e Fuorigiri `pilot-20261021-02`, inclusa release Android non firmata. Percorsi e verifiche nei registri dei prodotti. I riferimenti sotto ai binari non rigenerati descrivono la conclusione della sola revisione, prima di questa richiesta.

Revisione locale dei sorgenti correnti, richiesta per individuare difetti e applicare correzioni a basso rischio senza cambiare interfaccia o funzionalità. Repository inizialmente puliti; prove esclusivamente sintetiche. Non è una certificazione di sicurezza né un collaudo dei candidati già compilati.

## Stato e perimetro

- **Ammiraglia 0.1.0:** UI comune 0.2.2 e core Python 0.1.2. Gestione societaria, magazzino, account locali, archivio cifrato, collaborazione e calendari sono implementati; restano i gate di revisione indipendente e accettazione con dispositivi/provider reali indicati dal prodotto.
- **Fuorigiri 0.10.0:** UI comune 0.2.8 e core Python 0.1.2. Analisi, archivio revisionato, import/export, sincronizzazione e shell desktop/Android sono implementati. La qualifica dei candidati, dei provider e dei dispositivi rimane distinta dai test locali.
- Esaminati middleware API, autenticazione locale, selezione società, accessi operatore, lettura/cifratura archivio, riferimenti documentali, import CSV, export, ripristino e trasporti HTTP/WebDAV; controllati anche i principali pattern per esecuzione arbitraria, HTML diretto ed estrazione archivi nei sorgenti applicativi. Revisione mirata, non analisi esaustiva di ogni percorso o dipendenza.
- Nessuna modifica a UI, metodi scientifici, formati di archivio, credenziali o dati reali. Nessuna consegna common necessaria: le modifiche appartengono ai prodotti.

## Problemi corretti

| Prodotto | Problema verificato | Correzione |
|---|---|---|
| Entrambi | Un header di autenticazione contenente byte non ASCII provoca `TypeError` nel confronto del token e risposta interna d'errore. Non è stato dimostrato un bypass di autenticazione. | Rifiuto con HTTP 401 prima del confronto costante dei token ASCII. |
| Fuorigiri | Il CSV antropometrico principale include misure con stato `deleted`, diversamente dall'export esteso. | Esclusione delle misure eliminate; storico e archivio originale conservati. |
| Fuorigiri | CSV con virgolette non chiuse accettati dal parser permissivo; superamento della dimensione del campo provoca `csv.Error` non gestito. | Parser rigoroso e HTTP 422 comprensibile. Campi validi multilinea e virgolette raddoppiate preservati. Nessun innalzamento dei limiti. |
| Ammiraglia | `/api/state` rilegge l'archivio per ciascun gruppo; sugli archivi protetti comporta ulteriori decifrature e può produrre conteggi da letture diverse. | Membri calcolati dalla stessa istantanea già letta per la risposta: da 1+G letture di stato a una, con G gruppi. Gli altri controlli di accesso restano operativi. |
| Ammiraglia | Appartenenza a un gruppo statico verificata ripetutamente su una lista di ID. | Insieme di ID per il controllo di appartenenza, mantenendo ordine delle persone e filtri temporali. |
| Ammiraglia | La risposta HTTP d'errore del calendario non viene chiusa esplicitamente dopo la lettura. | Chiusura deterministica anche nel percorso d'errore; stato, intestazioni, corpo e retry conservati. |

Regressioni aggiunte per token anomali, CSV malformati e misure eliminate, conteggi da una sola lettura su archivio cifrato e chiusura della risposta HTTP. I tre nuovi casi Fuorigiri sono stati eseguiti anche prima delle correzioni e fallivano come previsto.

## Aspetti che richiedono una scelta ulteriore

1. **CSV grezzo Fuorigiri:** `reports.export_csv` conserva intenzionalmente il testo originale e lo dichiara nel manifest. Testi inizianti con caratteri da formula possono essere interpretati da un foglio di calcolo. Ammiraglia applica già una neutralizzazione alle celle. Per Fuorigiri serve un export distinto destinato ai fogli di calcolo, oppure una politica esplicita per preservare il reimport: aggiungere apostrofi al formato corrente cambierebbe i dati scambiati. Non modificato automaticamente.
2. **Carichi grandi:** alcune operazioni materializzano ancora liste, CSV o risposte in memoria. Il backup scalabile di Fuorigiri non rende automaticamente scalabili tutti gli endpoint. Servono misure con corpus grandi e limiti per operazione, preservando atomicità e compatibilità; nessun aumento arbitrario dei limiti o riscrittura introdotta qui.
3. **Grafici:** la build Fuorigiri segnala il chunk Plotly di circa 4,84 MB non compresso, già caricato separatamente. Ridurre i moduli grafici richiede verifica dei grafici supportati; non è una sostituzione priva di rischi per l'esperienza utente.
4. **Sicurezza operativa:** i controlli locali non qualificano account cloud reali, ripristino su PC sostitutivo, comportamento del vault OS su tutti i sistemi, ACL ulteriori o dispositivi Android reali. Restano i gate documentati dai prodotti.

## Verifiche

La baseline completa era verde: Ammiraglia 141 test Python, Fuorigiri 201 passati e uno saltato. Risultati finali dettagliati nei registri `club-lab/docs/VALIDAZIONE.md` e `test-analysis/docs/VERIFICA.md`.

- Test frontend: 6 Ammiraglia e 25 Fuorigiri superati; build TypeScript/Vite riuscite per entrambe. La build Ammiraglia ha richiesto una ripetizione fuori sandbox per il file temporaneo di Vite.
- `npm audit --json`, con accesso al registro, restituisce zero vulnerabilità note per entrambi i lockfile, incluse dipendenze di sviluppo. Questo risultato non copre Python, Qt, Android né il codice applicativo.
- `pip check` riuscito nei due ambienti: compatibilità delle dipendenze dichiarate, non scansione CVE. `pip-audit` non è installato nell'ambiente controllato; nessun esito CVE Python dichiarato.
- Verificatori standalone UI/core riusciti per entrambe; versioni Fuorigiri coerenti. Nessun riallineamento automatico della UI di Ammiraglia alla versione Android di Fuorigiri.
- Nessun cambiamento visivo: non ripetuto il collaudo browser. Nessun EXE, installer o APK rigenerato; i candidati esistenti non includono queste correzioni.

Le istruzioni AGENTS.md dei tre repository sono state rilette; non cambiano confini stabili o procedure, quindi non richiedono aggiornamenti in questa revisione.
