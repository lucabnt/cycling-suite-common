# Valutazione di librerie open per la suite · 19 novembre 2026

Analisi, nessuna dipendenza aggiunta. Criteri: licenza compatibile con GPL-3.0-or-later, funzionamento offline, nessuna nuova dipendenza nativa Python nell'APK (ogni wheel nativa richiede build Fedora, audit 16 KB e gate Android), lockfile con hash, codice rimosso maggiore di quello aggiunto. Le dipendenze solo di sviluppo non entrano negli installer né nell'APK.

## Raccomandate

| Libreria | Dove | Ambito | Motivo concreto | Costo |
|---|---|---|---|---|
| **Hypothesis** (MPL-2.0) | common, poi Fuorigiri e Ammiraglia | solo sviluppo | Test a proprietà sugli invarianti appena estratti: reversibilità di `csv_safety`, fork in `exchange.add_version`, ordine indipendente da `incremental`, apertura dei frame `crypto` alterati. In Fuorigiri: `apply_candidates` (ordine di arrivo degli eventi, conflitti), `csv_import.restore`; in Ammiraglia la fusione per campo. | Una dipendenza dev con hash; nessun impatto runtime. |
| **Regole Ruff aggiuntive** (già presente) | tre app e common | sviluppo | Oggi solo F/E9. Aggiungere `B` (bugbear: default mutabili, eccezioni ingoiate) e `UP` per la sintassi Python 3.12, una famiglia per commit, senza mescolarle con modifiche di comportamento. | Nessuna dipendenza nuova; correzioni iniziali. |
| **Playwright** (Apache-2.0) | Fuorigiri, poi Ammiraglia | sviluppo | Le istruzioni richiedono una verifica GUI oltre ai test dei modelli: un percorso ripetibile su archivio QA nuovo (apertura società, import CSV, dettaglio test, dialoghi annidati, export) sostituisce i passaggi manuali più frequenti. | Il download dei browser richiede rete al primo uso; tenerlo fuori dal workflow `verify` se non c'è cache. |
| **Vitest + Testing Library** (MIT) | common UI, poi app | sviluppo | I test `node --test` coprono i modelli, non i componenti. Dialog, TimeInput e paginazione del common sono i primi candidati: oggi le regressioni (scorrimento, cancel annidato) sono verificate con test DOM fatti a mano. | Dipendenze dev; configurazione Vite già presente. |
| **pip-audit** (Apache-2.0) | tre app | controllo manuale pre-release | Confronta i lockfile con gli avvisi di sicurezza noti prima di un candidato. Complementare a `lock_hashes.py`, che prova l'integrità e non la vulnerabilità. | Richiede rete; non va nel percorso offline. |

## Da valutare in un secondo momento

- **TanStack Query** (MIT), solo Fuorigiri: semplificherebbe cache, retry e polling delle chiamate (`useSyncJob`, 19 chiamate in `main.tsx`). Conviene durante la suddivisione di `main.tsx` (2.814 righe), non come intervento isolato. Non va nella UI comune, che non fa rete.
- **openapi-typescript** (MIT): utile solo dopo aver dichiarato modelli di risposta nelle rotte FastAPI; oggi le risposte sono dizionari e il generatore tipizzerebbe quasi solo le richieste.
- **pyright** in modalità base, solo per `packages/core`: moduli piccoli e stabili, buon rapporto costo/beneficio. Nelle app il codice non è annotato e il beneficio iniziale sarebbe basso.
- **uv** per i lockfile: potrebbe sostituire `lock_hashes.py`, ma cambia lo strumento di tre app e del workflow con hash. Solo con una decisione dedicata.

## Non raccomandate

- **react-i18next / Lingui**: l'`i18n.ts` di Fuorigiri usa il testo italiano come chiave, come gettext; una libreria aggiungerebbe plurali e interpolazione non richiesti oggi. Più utile un controllo che segnali le stringhe passate a `tr()` senza traduzione inglese.
- **Router** (react-router, wouter): navigazione e cronologia del tasto Indietro Android sono già modellate (`androidBackModel`, TD-99–104). Un router richiederebbe di riscrivere queste regole senza rimuovere codice.
- **tenacity**: il ritardo esponenziale è ora `cycling_suite.jobs.backoff` (tre righe, testato); i trasporti hanno già ritentativi propri.
- **PyNaCl, pyrage o altre librerie crittografiche native**: duplicano `cryptography`, già nel gate Android, e aggiungerebbero wheel native da qualificare.
- **Dependabot per pip**: le wheel comuni sono vendorizzate e i lockfile hanno file `.hashes` derivati; le PR automatiche fallirebbero il controllo. Accettabile solo per `github-actions` (azioni fissate per SHA) e per npm nelle repository pubblicate su GitHub.

## Ordine proposto

1. Hypothesis nel common sugli invarianti di core 0.2.0.
2. Ruff `B` nelle tre app, un commit per app.
3. Playwright in Fuorigiri su archivio QA nuovo.
4. Vitest per i componenti comuni.
5. pip-audit nella checklist dei candidati.
