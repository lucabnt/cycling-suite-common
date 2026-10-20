# @cycling-suite/ui 0.2.2

React 19, moduli ESM, TypeScript, GPL-3.0-or-later. Pacchetto iniziale di componenti comuni a Fuorigiri e Ammiraglia.

```tsx
import {Field, DataTable, SuiteBranding} from '@cycling-suite/ui';
import '@cycling-suite/ui/theme.css';
import '@cycling-suite/ui/components.css';

<Field label="Nome"><input /></Field>
<DataTable rows={[{id:'1',name:'Esempio',value:0}]} columns={[
  {key:'name',label:'Nome'}, {key:'value',label:'Valore'}
]} />
<SuiteBranding productName="Ammiraglia" />
```

Il tema esporta variabili `--suite-*` e gli alias Fuorigiri `--brand`, `--ink`, `--surface`, `--border`. I CSS dei componenti sono limitati alle classi dei componenti: non azzerano globalmente tutti gli elementi HTML. Le pagine conservano il proprio layout; i CSS comuni precedono gli stili specifici.

`SortableTable` accetta thead/tbody React, per conservare le tabelle dichiarative di Fuorigiri. Per nuovo codice preferire `DataTable`, che ordina i valori originali delle righe. Null/undefined vanno in fondo in entrambe le direzioni; zero e false non diventano mancanti. Il formato di numeri/date/unità è responsabilità del render della colonna. Dati omogenei e chiavi `id` stabili sono raccomandati.

`Field` avvolge il controllo nel label; per un controllo separato passare `htmlFor` e il corrispondente `id`. `SuiteBranding` include il logo locale, senza URL da configurare: Vite lo incorpora come risorsa del bundle. Cambiare productName non modifica la società fondatrice.

Nessuna richiesta HTTP, gestione di sessioni, permessi backend, storage o calcolo fisiologico. Gli stati disabilitati nell’interfaccia non sostituiscono la verifica dei permessi nel backend.


## Shell, finestre e tempi (0.2.2)

Importare `theme.css`, `components.css`, `application.css`, poi il CSS delle sole pagine specifiche. `application.css` è opt-in: definisce controlli globali, shell `.app`, sidebar, navigazione, intestazione, titoli, griglia moduli, liste, tabelle e schede riepilogative. Non mantenerne copie nelle app. Nome, logo prodotto e voci di menu sono contenuti delle app; i token sono comuni.

`Dialog` accetta `title`, `children`, `onClose`, `wide` (default true), `editor` (default false), `busy` e `locale` (`it`/`en`). Usa dialog nativo, sfondo opaco, focus iniziale/ripristinato, Esc, testata fissa e conferma di scarto negli editor. `busy` blocca Esc e chiusura; il salvataggio riuscito resta responsabilità dell'app. Non avvolgere altre modali native dentro il contenuto senza una necessità funzionale.

`TimeInput` riceve `label`, `value` in secondi o null, `onChange` e `locale`. `clock`, `parseClock` e `validTimes` conservano zero, mancanti, frazioni e validazione mm:ss. Nessun contenuto scientifico o glossario di dominio è trasferito alla libreria.
