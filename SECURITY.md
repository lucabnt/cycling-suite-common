# Sicurezza

Questa repository contiene librerie condivise da Fuorigiri, Ammiraglia e A Ruota: la UI React comune e il runtime Python `cycling-suite-core` (portachiavi del sistema operativo, trasporti cartella/WebDAV, primitive crittografiche, scritture atomiche, CSV sicuro, job di sync).

## Segnalare una vulnerabilità

Non aprire una issue pubblica. Usare la segnalazione privata di GitHub: scheda **Security** → **Report a vulnerability**.

Indicare, se possibile:

- modulo o componente coinvolto e versione (`packages/core/pyproject.toml`, `packages/ui/package.json`);
- passi per riprodurre, idealmente con dati sintetici;
- impatto atteso (riservatezza, integrità, disponibilità).

Non includere dati reali di atleti, credenziali o archivi cifrati reali. Si tratta di un progetto volontario: la risposta avviene appena possibile, senza tempi garantiti.

## Versioni supportate

Si correggono soltanto l'ultima versione della UI e quella del core. Le applicazioni ricevono le correzioni con una nuova versione e una consegna esplicita (`scripts/sync-ui.mjs`, `scripts/sync-core.py`).

## Perimetro

Formati di backup, inviti, firme e sync, modelli di accesso e server restano nelle singole applicazioni: le vulnerabilità in quelle parti vanno segnalate nella repository del prodotto interessato, se pubblica, oppure qui indicando l'applicazione.
