# Changelog

## 15 novembre 2026 — strumenti di consegna (revisione tecnica Fuorigiri, RT-18/RT-19)

- Nuovo `scripts/lock-hashes.py`, consegnato da `sync-core.py` alle app come `scripts/lock_hashes.py` accanto a `verify_core.py`. Per ogni lockfile `requirements*.lock` o `requirements-lock*.txt` genera da PyPI un file `.hashes` per `pip install --require-hashes` e ne controlla offline la coerenza. Esclude `requirements-common.txt`: la wheel comune si installa con `--no-deps --no-index` ed è già verificata da `verify_core.py`. `sync-core.py` continua a non scrivere hash nei requisiti.
- Workflow `verify.yml` con azioni fissate per SHA del commit e versione in commento.
- Nuovo test: i moduli JavaScript della UI comune non usano `eval`, `new Function` né script in linea, così restano compatibili con una Content-Security-Policy senza `unsafe-eval`.
- Core 0.1.2 e UI 0.2.9 invariati: nessuna nuova versione. Consegnato soltanto a Fuorigiri; Ammiraglia e A Ruota non aggiornati.

## 8 novembre 2026 — UI 0.2.9

- Dialog rilascia il blocco dello scorrimento solo alla chiusura dell’ultima finestra, indipendentemente dall’ordine di smontaggio di editor e conferme. Ripristino dello stile originale e rilascio idempotente; quattro regressioni coprono sei permutazioni, annullamento e replay.

## Riallineamento documentazione e catalogo Android — 21 ottobre 2026

Confronto con Fuorigiri `30d0f0a`, convenzioni TD-98–107. Sorgenti UI 0.2.8 già coerenti con il tarball consumato: nessuna nuova versione o modifica ai byte della libreria. Aggiornati README, architettura, guida Android e matrice dei consumatori; aggiunti contratti API, catalogo Android interattivo e regressioni per pagina controllata, superfici immersive e stati recuperabili. Esiti delle verifiche in [UI_ANDROID.md](docs/UI_ANDROID.md). Ammiraglia conserva UI 0.2.2; nessun installer o APK rigenerato.

# 0.2.8 — 21 ottobre 2026

Variante brand-end per marchi con testo allineato a destra. Fuorigiri Android dispone nome/tagline prima dell’icona, a destra nella testata.

# 0.2.7 — 21 ottobre 2026

Dialog fullscreen con chiusura flottante e titolo accessibile conservato, ChartFrame fullscreen e FloatingPanel per comandi richiamabili. Marchio orizzontale con icona non comprimibile. Consegna a Fuorigiri soltanto.

# 0.2.6 — 21 ottobre 2026

Cancel dei dialoghi annidati non si propaga al genitore; focus senza spostare lo scroll. ChartFrame supporta comandi sotto il grafico. Testata Android va a capo anche in landscape.

# 0.2.5 — 21 ottobre 2026

Densità Android moderata, testata/contesto persistenti, ChartFrame e LoadingState accessibili, animazioni ridotte. Consegna esplicita a Fuorigiri soltanto; prove nel prodotto.

# Changelog

## 0.1.0 — 18 ottobre 2026

- Repository comune autonoma, GPL-3.0-or-later, con libreria React ESM, tipi TypeScript e CSS espliciti.
- Tema a token, Field, DataTable, SortableTable, footer societario fisso con nome applicativo variabile e logo originale locale.
- Ordinamento con mancanti sempre in fondo e controlli di tabella che non inviano i form; zero e false preservati.
- Catalogo interattivo per Fuorigiri/Ammiraglia, dati fittizi, stato visualizzatore soltanto dimostrativo.
- Build/test/pack e guida di consumo tramite artefatto versionato; nessun servizio backend, migrazione dati o pubblicazione remota automatica.
# 20 ottobre 2026 — core Python 0.1.2

Estratti da Fuorigiri portachiavi OS, trasporti immutabili cartella/WebDAV, lock di istanza e shell Qt. Wheel deterministica con sorgenti/licenza, consegna automatica e verifica dei consumatori Fuorigiri/Ammiraglia. UI 0.2.2 invariata; archivi, autorizzazioni e formati restano applicativi. [Guida](docs/CORE_PYTHON.md).

## UI 0.2.3 — Android, 20 ottobre 2026

- RecordCards paginati, filtri richiudibili e FormActions riutilizzabili; controlli touch e tastiere numeriche Android, scorrimento al campo invalido. Nessuna dipendenza da dati o storage di prodotto. Consegna locale esplicita a Fuorigiri; nessuna pubblicazione o aggiornamento implicito delle altre app.

## UI 0.2.4 — ritorno agli elenchi

- Paginazione controllabile dal prodotto per conservare pagina e filtri quando si torna da un profilo; allineamento orizzontale delle etichette checkbox nei moduli Android.
