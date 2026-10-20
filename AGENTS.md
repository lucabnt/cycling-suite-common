# Cycling Suite Common — istruzioni

Common è l'unica fonte di verità delle parti condivise di Fuorigiri (`test-analysis`) e Ammiraglia (`club-lab`). Le applicazioni mantengono repository, dati e build autonomi.

- Modificare qui token, shell/controlli, liste/tabelle/riepiloghi, Field, Dialog, tempi e branding societario. Non copiare implementazioni o CSS nelle app. Le app conservano adattatori di lingua, nomi/loghi prodotto, menu e layout/funzioni specifici.
- Leggere le istruzioni della repository sorella prima di modificarla; preservare dati e modifiche preesistenti. Non delegare ad agenti senza richiesta esplicita.
- Incrementare la versione di `packages/ui` prima di cambiare i byte di una versione già consegnata; aggiornare la dipendenza del catalogo e il lockfile. Non cambiare le versioni prodotto per il solo aggiornamento della libreria.
- Verificare `npm test`, `npm run build` e il browser per cambiamenti visivi. Aggiornare le app con `npm run sync:ui -- --app ../club-lab --app ../test-analysis`; eseguire poi i test/build delle due app e `npm run sync:ui -- --app ../club-lab --app ../test-analysis --check`.
- `--check` richiede versione e impronta sorgenti correnti, oltre a integrità tarball/lockfile. Le verifiche standalone delle app restano indipendenti dal clone common. Non modificare direttamente il vendor.
- Import CSS: tema, componenti, application.css, poi layout specifici. Per i cambi comuni usare nuova versione e consegna esplicita, mai un branch mobile o un percorso a una repository sorella nelle dipendenze.
- Niente dati reali, rete o storage nella UI comune. Preservare GPL, sorgenti e branding societario fisso. Il codice comune non condivide automaticamente archivi, autorizzazioni o chiavi.
- Riferimenti: README.md, docs/ARCHITETTURA.md, docs/INTEGRAZIONE.md e docs/RIALLINEAMENTO_UI.md. Mantenere queste istruzioni aggiornate quando cambiano i confini stabili.
