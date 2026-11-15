# Verifica iniziale 0.1.0

## 15 novembre 2026 — hash dei lockfile e compatibilità CSP

- `npm test`: 18 test UI/consegna superati, compreso il nuovo controllo CSP sui moduli di `packages/ui/dist`; 4 test Python del core superati, compreso il nuovo test di `lock-hashes.py` (lockfile con `-r` tra lockfile, `requirements-common.txt` escluso, marcatore di piattaforma conservato, versione diversa segnalata, file `.txt` non di lock ignorato). `npm run build` riuscito.
- Consegna a Fuorigiri: `sync-core.py --app ../performance-lab --install` e `--check` riusciti; wheel 0.1.2 identica. In Fuorigiri `lock_hashes.py --write` ha prodotto gli hash di 59 pacchetti e una installazione simulata con `--require-hashes` ha risolto tutti i pacchetti.
- Non eseguiti: consegna e prove in Ammiraglia e A Ruota, workflow su GitHub.

## 26 ottobre 2026 — installer Windows Ammiraglia

Prodotto anche il setup `club-lab/dist/candidates/ammiraglia-20261026-pilot-02-installer/Ammiraglia-0.1.0-windows-x64-setup.exe`, 180354103 byte, SHA-256 `a2f3819d11addc5867049aaaff275e4c4ab157482fb0b8f6b5b89563a14fd3cf`. Compilazione Inno dal bundle 02 congelato con verifica dei file prima/dopo, AppId e installazione per utente conservati. Consegna separata con sorgenti applicativi/packaging, manifest e checksum verificati; il portabile precedente rimane immutato. Nessuna modifica a runtime/UI/core, installazione sul profilo operativo, firma Authenticode o pubblicazione. Installazione/aggiornamento/disinstallazione su PC pulito restano nella checklist del prodotto; non ripetute suite applicative per il solo confezionamento del medesimo bundle.

## 25 ottobre 2026 — allineamento Ammiraglia e preparazione pilot

- UI 0.2.8 esistente consegnata ad Ammiraglia e riverificata in Fuorigiri tramite `sync:ui`, senza cambiare byte o versione della libreria. Core 0.1.2 invariato e installazioni verificate. Controlli `sync:ui --check` e `sync-core.py --check` finali riusciti su entrambe; matrice e documentazione Android aggiornate separando consumo e adozione nativa.
- Common: 13 test UI/consegna e 3 test Python superati, build libreria/catalogo riuscita. Ammiraglia: 147 test Python finali e 6 frontend superati, build frontend e Windows riuscite. Fuorigiri: 252 Python superati/1 saltato e 34 frontend superati, build riuscita sul checkout locale in evoluzione, preservato. Warning noti: Starlette/httpx, fixture ZIP duplicata/cache pytest e dimensione Plotly; nessun nuovo audit dipendenze dichiarato.
- Ammiraglia implementa nel proprio backend la preferenza locale della società con API autenticata, scrittura atomica, ID validati e nessun fallback automatico. Quattro nuove regressioni, inclusa assenza del file archivio con ID ancora presente: nessuna base vuota sostitutiva creata. Browser su corpus sintetici nuovi: scelta iniziale, scheda/elenco, anteprima report, editor con scarto e ripresa, riapertura della seconda società dopo arresto e cambio porta/token/origine. Verificato anche avvio/apertura esplicita con archivio temporaneamente non disponibile. Nove catture README ricatturate e ispezionate, più evidenze di riapertura e archivio assente.
- Candidato portabile corrente `club-lab/dist/candidates/ammiraglia-20261025-pilot-02-windows-x64-portable.zip`, SHA-256 `ec1b7b383689835bc0ae8d8bdc771051565af4e34cb83534498a86ccb98f448c`. Include il controllo aggiuntivo sul file archivio. Smoke dell'EXE reale con PATH limitato a Windows e dati QA nuovi riuscito; frontend incluso identico byte per byte alla build verificata. Consegna con sorgenti locali congelati, log dei 147 test, manifest/provenienza, checksum verificati anche dentro lo ZIP e launcher su profili QA distinti. Conservato il precedente 01 (SHA-256 `631da8361a1bce776f0f069ba5eb822437a53d699bbd884d1fc6240c7765f40e`) e le RC precedenti; riconfezionamento sullo stesso candidato rifiutato. Nessun setup o pubblicazione.
- Checklist e registri restano nei prodotti. Nessun dato reale aperto; PC pulito, due PC/provider reali, revisione indipendente, licenza complessiva e accettazione staff rimangono gate aperti. La disponibilità del candidato non autorizza automaticamente il pilot con dati personali.

Le sezioni successive conservano i collaudi precedenti.

18 ottobre 2026, Windows, Node 24/npm 11.

- Quattro test Node passati: numeri/mancanti in entrambe le direzioni, zero/false, pulsanti che non inviano form, associazione dei label/escape e footer locale con nome applicativo variabile.
- Build TypeScript dichiarazioni/ESM e catalogo Vite completate. Logo emesso localmente nel bundle, stesso SHA256 del logo originale Fuorigiri.
- Catalogo provato in browser: cambio Fuorigiri/Ammiraglia, branding fisso, campi disabilitati nella simulazione visualizzatore, ordinamento 250/0/mancante. Il catalogo non verifica permessi backend.
- Fuorigiri compilato contro il tarball, senza import da cartelle sorgenti esterne; quattro componenti e i CSS comuni sostituiscono le copie locali. Suite backend Fuorigiri: 117 passati, warning preesistente Starlette/httpx.
- CI dichiarata, non eseguita su un servizio remoto. Linux, Android, tastiera/screen reader completi e integrazione nella repository Ammiraglia non collaudati. Nessun nuovo installer desktop prodotto per questa estrazione.
## 20 ottobre — core Python 0.1.2

Superati 8 test UI/consegna e 3 test core (wheel deterministica/licenza, namespace vault/no fallback, isolamento/pubblicazione immutabile/lock). Build UI/catalogo riuscite; `sync-core.py --check` e `sync:ui --check` riusciti per Fuorigiri e Ammiraglia. I verificatori standalone controllano checksum, sorgenti installate e versione dichiarata senza un clone fratello. Consumatori: Ammiraglia 105 backend/5 frontend; Fuorigiri 201 backend + 1 saltato/19 frontend. Smoke desktop di entrambi e roundtrip sintetico Windows Vault riusciti; bundle e installer Ammiraglia prodotti localmente. Provider reali, PC pulito e Android/Linux restano qualifiche distinte non effettuate.
