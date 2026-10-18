import {useState} from 'react';
import {createRoot} from 'react-dom/client';
import {Field,DataTable,SuiteBranding} from '@cycling-suite/ui';
import '@cycling-suite/ui/theme.css';
import '@cycling-suite/ui/components.css';
import './style.css';

const rows=[{id:'1',athlete:'Atleta sintetico A',power:250,date:'2026-10-18'},{id:'2',athlete:'Atleta sintetico B',power:null,date:'2026-10-16'},{id:'3',athlete:'Atleta sintetico C',power:0,date:'2026-10-15'}];
function Catalog(){
 const [product,setProduct]=useState('Fuorigiri Performance Lab'),[query,setQuery]=useState(''),[readOnly,setReadOnly]=useState(false);
 return <div className="catalog"><header><p>CYCLING SUITE · CATALOGO UI 0.1</p><h1>Due applicazioni, componenti comuni.</h1><p>Catalogo dimostrativo offline. Tutti i dati sono sintetici.</p></header><section className="panel"><h2>Contesto applicativo</h2><Field label="Applicazione"><select value={product} onChange={e=>setProduct(e.target.value)}><option>Fuorigiri Performance Lab</option><option>Ammiraglia</option></select></Field><p className="hint">{product} · Il nome dell’app varia; logo societario e attribuzione rimangono fissi.</p><label className="choice"><input type="checkbox" checked={readOnly} onChange={e=>setReadOnly(e.target.checked)}/>Simula visualizzatore</label><Field label="Nome del gruppo"><input disabled={readOnly} placeholder="Esempio: Allievi 2026"/></Field><button disabled={readOnly}>Esempio azione {readOnly?'non disponibile':'disponibile'}</button><p>Questo controllo illustra lo stato UI; non applica autorizzazioni backend.</p></section><section className="panel"><h2>Tabelle, filtri e dati mancanti</h2><Field label="Filtra atleta"><input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Cerca un atleta sintetico"/></Field><DataTable rows={rows.filter(r=>r.athlete.toLowerCase().includes(query.toLowerCase()))} columns={[{key:'athlete',label:'Atleta'},{key:'power',label:'Potenza · W'},{key:'date',label:'Data'}]}/><p>Ordina la potenza in entrambe le direzioni: i valori mancanti restano in fondo e zero rimane zero.</p></section><SuiteBranding productName={product}/></div>;
}
createRoot(document.getElementById('root')!).render(<Catalog/>);
