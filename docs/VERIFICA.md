# Verifica iniziale 0.1.0

18 ottobre 2026, Windows, Node 24/npm 11.

- Quattro test Node passati: numeri/mancanti in entrambe le direzioni, zero/false, pulsanti che non inviano form, associazione dei label/escape e footer locale con nome applicativo variabile.
- Build TypeScript dichiarazioni/ESM e catalogo Vite completate. Logo emesso localmente nel bundle, stesso SHA256 del logo originale Fuorigiri.
- Catalogo provato in browser: cambio Fuorigiri/Ammiraglia, branding fisso, campi disabilitati nella simulazione visualizzatore, ordinamento 250/0/mancante. Il catalogo non verifica permessi backend.
- Fuorigiri compilato contro il tarball, senza import da cartelle sorgenti esterne; quattro componenti e i CSS comuni sostituiscono le copie locali. Suite backend Fuorigiri: 117 passati, warning preesistente Starlette/httpx.
- CI dichiarata, non eseguita su un servizio remoto. Linux, Android, tastiera/screen reader completi e integrazione nella repository Ammiraglia non collaudati. Nessun nuovo installer desktop prodotto per questa estrazione.
