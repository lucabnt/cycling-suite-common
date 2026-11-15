# Runtime Python condiviso — 20 ottobre 2026

`cycling-suite-core` 0.1.2 affianca la UI 0.2.2. Estratti dai sorgenti Fuorigiri 0.10.0:

- `credentials`: selezione esplicita Windows Vault / Secret Service, namespace per prodotto e nessun fallback su file;
- `transports`: cartella e WebDAV HTTPS per oggetti immutabili, limiti, pubblicazione condizionale, rilettura e retry;
- `instance`: lock di processo rilasciato dal sistema operativo;
- `desktop`: finestra Qt, download, navigazione locale e apertura esterna controllata, compreso `mailto:`.

I trasporti condivisi non autorizzano eventi: firme, identità, canali, inviti, revoche e journal appartengono alle app. I loro archivi e formati di scambio restano distinti. La UI comune continua a non avere rete o storage. OAuth cloud, calcoli scientifici e il formato di backup Fuorigiri non sono stati copiati in Ammiraglia.

## Consegna riproducibile

Da questa repository, con gli ambienti Python delle tre app già disponibili:

```powershell
python scripts/sync-core.py --app ../club-lab --app ../performance-lab --app ../training-lab --install
python scripts/sync-core.py --app ../club-lab --app ../performance-lab --app ../training-lab --check
python -m unittest discover -s tests -p test_core.py -v
```

La versione è in `packages/core/pyproject.toml` e `src/cycling_suite/__init__.py`: aggiornarle insieme prima di cambiare una wheel già prodotta. Il costruttore produce una wheel deterministica con sorgenti, RECORD, licenza e NOTICE. Rifiuta di cambiare i byte di una versione già prodotta.

La consegna copia l'artefatto in `vendor/`, registra versione/SHA256/provenienza, aggiorna il requisito Python, `requirements-common.txt` e i lockfile presenti, e installa offline solo quando richiesto con `--install`. `--check` confronta anche le sorgenti correnti e verifica l'installazione di ciascun consumatore. Lo script standalone `scripts/verify_core.py` delle app verifica wheel, licenza, versione dichiarata, sorgenti installate e dipendenza senza accedere al clone common.

Da un clone autonomo dell'app:

```powershell
python -m pip install -r requirements-common.txt
python scripts/verify_core.py
```

Installazione con hash (dal 15 novembre 2026): la consegna copia anche `scripts/lock_hashes.py`. Nell'app, `python scripts/lock_hashes.py --write` crea per ogni lockfile `requirements*.lock` o `requirements-lock*.txt` un file `.hashes` con gli SHA-256 di PyPI; `python scripts/lock_hashes.py` ne verifica offline la coerenza. Installare con `pip install --require-hashes -r <lock>.hashes`, poi `pip install --no-deps --no-index -r requirements-common.txt`. Non aggiungere hash a `requirements-common.txt`: `sync-core.py` lo riscrive e i lockfile senza hash smetterebbero di installarsi. I file consegnati non si riformattano nell'app: escluderli dal formatter.

Non modificare il vendor a mano. Non usare import da repository sorelle o dipendenze a percorsi assoluti. Le dipendenze native del desktop e del portachiavi restano responsabilità di installazione delle app; il pacchetto comune usa import lazy per non imporre Qt ai server web.

## Compatibilità preservata

Fuorigiri conserva adattatori per i vecchi nomi di canale/cartella, i servizi del portachiavi `Fuorigiri.WebDAV` e `Fuorigiri.Cloud`, l'adattatore Android esistente e il nome del lock. Ammiraglia usa namespace separati. Nessun archivio reale migrato durante il collaudo.

## Consumatori correnti — 2 novembre 2026

Ammiraglia (`club-lab`), Fuorigiri (`performance-lab`, già `test-analysis`) e A Ruota (`training-lab`) consumano core 0.1.2 e UI 0.2.8. Il controllo common `--check` ha verificato per tutti e tre wheel, derivazione corrente e installazione Python autonoma. Nessuna nuova wheel necessaria per le recenti modifiche dei flussi applicativi.
