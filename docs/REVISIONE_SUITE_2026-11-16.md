# Revisione delle derivazioni della suite · 16 novembre 2026

Confronto dei checkout locali di Common (`f5e51c0`), Fuorigiri (`3794786`), Ammiraglia (`71e9b62`) e A Ruota (`032594e`). Per Fuorigiri e Ammiraglia sono state lette anche le modifiche locali. La [matrice di integrazione](INTEGRAZIONE.md) registra i controlli di consegna eseguiti. Le prove di prodotto citate nelle rispettive revisioni appartengono ai candidati lì indicati.

| App | Progresso rilevante per Common | Confine da conservare |
|---|---|---|
| Fuorigiri | Rotte suddivise per area, ottimizzazioni di stato e sync, backup v3 protetto da password e candidato Windows/Android. Il PHV longitudinale è ora raggiungibile dall'app. | Motori scientifici, contenuto ZIP v3 e ripristino restano del prodotto. |
| Ammiraglia | La revisione R1–R14 ha portato diagnostica, copie locali, interventi su accessi e archivio. Il pilot prevede una società e un trasporto qualificato. | Le copie devono rispettare il ciclo delle passphrase e il recupero degli accessi. La qualifica con due PC e provider reale resta nel prodotto. |
| A Ruota | Diagnostica a rotazione, conservazione degli snapshot su due livelli, backup desktop cifrato e confronto Intervals esteso a tutte le sottofinestre. | Pacchetto firmato, limiti di memoria, criteri di confronto e qualifica del picker Android dipendono dal prodotto. |

## Prima della derivazione del backup

In entrambi i moduli `backup_crypto.py`, `encrypt_file` apre la sorgente prima della destinazione. Se la sorgente manca, il gestore dell'errore cancella il percorso di destinazione anche quando il file esisteva prima della chiamata. Riprodotto separatamente nei due ambienti Python con una directory temporanea, una sorgente assente e una destinazione sintetica contenente una sentinella. Il risultato riguarda la chiamata diretta alla funzione. La raggiungibilità dai flussi utente va verificata nei rispettivi adattatori.

Priorità immediata per entrambi i prodotti: limitare la pulizia al file effettivamente creato dalla chiamata. Coprire con regressioni la sorgente assente con destinazione preesistente, la collisione in apertura e l'errore di scrittura dopo la creazione.

## Cosa derivare

**Cifratura a blocchi, Fuorigiri e A Ruota.** A Ruota dichiara la derivazione nel proprio modulo. Chiave da scrypt, nonce dall'indice, autenticazione di intestazione/indice/ultimo blocco e lettura dei blocchi AES-GCM hanno già due consumatori. Propongo di derivare queste operazioni nel core dopo la correzione, mantenendo facoltativa la dipendenza da `cryptography` per chi usa gli altri moduli. Le app possiedono ancora magic, versione, tipo di contenuto, suffissi, limiti scrypt, messaggi e pubblicazione/ripristino del file. Il massimo di `n` accettato in lettura è oggi 2²⁰ in Fuorigiri e 2¹⁷ in A Ruota. Prima della consegna verificare file storici di ciascun formato, nuova scrittura leggibile dal lettore precedente, password errata, troncamento e alterazione dell'intestazione. La proposta estende il core soltanto alle primitive e richiederebbe un aggiornamento esplicito di ADR-004.

**Diagnostica, Ammiraglia e A Ruota.** Esistono due usi, ma i contratti differiscono. Ammiraglia invia posizione e classe dell'eccezione a `uvicorn.error` e il desktop configura `server.log`. A Ruota usa un file a rotazione, un codice operativo e frame privi del messaggio dell'eccezione. Prima di estrarre, concordare quali campi possano essere registrati e provare il comportamento a disco indisponibile con entrambi i chiamanti. Percorso, nome del registro e configurazione del server spettano all'app.

**Consegna degli strumenti.** Oggi `sync-core.py --check` confronta la wheel e poi esegue il verificatore locale. La consegna copia anche `verify_core.py` e `lock_hashes.py`, ma il controllo non confronta queste copie con le sorgenti. Estendere il controllo ai due script prima di eseguire il verificatore locale, con una regressione su copia alterata. È una modifica allo strumento di consegna, indipendente dal versionamento della wheel.

**UI e flussi applicativi.** La verifica di consegna e le revisioni considerate non evidenziano una nuova primitiva React da pubblicare. Per la suddivisione delle rotte, i test dei modelli frontend e i workflow con hash basta riusare il metodo. Cache degli archivi, firme, sync, integrazione Intervals e ciclo di vita dei server hanno invarianti diversi nelle tre app.
