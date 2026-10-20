# Verifica iniziale 0.1.0

18 ottobre 2026, Windows, Node 24/npm 11.

- Quattro test Node passati: numeri/mancanti in entrambe le direzioni, zero/false, pulsanti che non inviano form, associazione dei label/escape e footer locale con nome applicativo variabile.
- Build TypeScript dichiarazioni/ESM e catalogo Vite completate. Logo emesso localmente nel bundle, stesso SHA256 del logo originale Fuorigiri.
- Catalogo provato in browser: cambio Fuorigiri/Ammiraglia, branding fisso, campi disabilitati nella simulazione visualizzatore, ordinamento 250/0/mancante. Il catalogo non verifica permessi backend.
- Fuorigiri compilato contro il tarball, senza import da cartelle sorgenti esterne; quattro componenti e i CSS comuni sostituiscono le copie locali. Suite backend Fuorigiri: 117 passati, warning preesistente Starlette/httpx.
- CI dichiarata, non eseguita su un servizio remoto. Linux, Android, tastiera/screen reader completi e integrazione nella repository Ammiraglia non collaudati. Nessun nuovo installer desktop prodotto per questa estrazione.
## 20 ottobre — core Python 0.1.2

Superati 8 test UI/consegna e 3 test core (wheel deterministica/licenza, namespace vault/no fallback, isolamento/pubblicazione immutabile/lock). Build UI/catalogo riuscite; `sync-core.py --check` e `sync:ui --check` riusciti per Fuorigiri e Ammiraglia. I verificatori standalone controllano checksum, sorgenti installate e versione dichiarata senza un clone fratello. Consumatori: Ammiraglia 105 backend/5 frontend; Fuorigiri 201 backend + 1 saltato/19 frontend. Smoke desktop di entrambi e roundtrip sintetico Windows Vault riusciti; bundle e installer Ammiraglia prodotti localmente. Provider reali, PC pulito e Android/Linux restano qualifiche distinte non effettuate.
