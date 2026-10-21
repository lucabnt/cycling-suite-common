import test from 'node:test';
import assert from 'node:assert/strict';
import {createElement as h} from 'react';
import {renderToStaticMarkup as render} from 'react-dom/server';
import {RecordCards,FormActions,CollapsibleFilters,ChartFrame,LoadingState,FloatingPanel,Dialog} from '../packages/ui/dist/index.js';
test('compact records limit the initial DOM and retain zero and missing labels',()=>{
 const items=Array.from({length:45},(_,i)=>({id:String(i),title:'Rider '+i,details:[{label:'Power',value:i===0?0:'—'}]}));
 const html=render(h(RecordCards,{items,onOpen(){},actionLabel:'Open',pageSize:20}));
 assert.equal((html.match(/<article/g)||[]).length,20);
 assert.match(html,/>0<\/dd>/);assert.match(html,/>—<\/dd>/);
 assert.match(html,/1–20 \/ 45/);assert.match(html,/type="button"/);
 assert.doesNotMatch(html,/Rider 20/);
});

test('controlled pagination restores the selected page and clamps after records disappear',()=>{
 const items=Array.from({length:12},(_,i)=>({id:String(i),title:'Record '+i,details:[]}));
 const props={items,onOpen(){},actionLabel:'Apri',pageSize:5,pageIndex:2};
 const restored=render(h(RecordCards,props));
 assert.match(restored,/11–12 \/ 12/);assert.doesNotMatch(restored,/>Record 0</);
 const reduced=render(h(RecordCards,{...props,items:items.slice(0,3)}));
 assert.match(reduced,/>Record 0</);assert.equal((reduced.match(/<article/g)||[]).length,3);
});

test('immersive surfaces preserve accessible names, close control and initially collapsed tools',()=>{
 const html=render(h(Dialog,{title:'Vista ampia',fullscreen:true,onClose(){}},h(ChartFrame,{label:'Valori sintetici',fullscreen:true},h(FloatingPanel,{label:'Comandi'},'Dati'))));
 assert.match(html,/aria-label="Vista ampia"/);assert.match(html,/aria-label="Chiudi finestra"/);
 assert.match(html,/suite-dialog-fullscreen/);assert.match(html,/suite-chart-fullscreen/);
 assert.match(html,/<details class="suite-floating-panel"><summary>Comandi<\/summary>/);
});

test('chart commands can follow the surface and loading failures offer a truthful retry',()=>{
 const html=render(h(ChartFrame,{label:'Grafico',toolsAfter:true,tools:h('button',{type:'button'},'Esplora')},h('div',null,'Superficie')));
 assert.ok(html.indexOf('Superficie')<html.indexOf('Esplora'));
 const loading=render(h(LoadingState,{title:'Avvio',detail:'Fase corrente'}));
 assert.match(loading,/role="status"/);assert.doesNotMatch(loading,/progress|%/);
 const failed=render(h(LoadingState,{title:'Errore',detail:'Dati disponibili',retry(){},retryLabel:'Riprova'}));
 assert.match(failed,/role="alert"/);assert.match(failed,/>Riprova<\/button>/);
});
test('filter and action containers preserve native validation and accessible controls',()=>{
 const html=render(h('form',null,h(CollapsibleFilters,{label:'Filters'},h('input',{required:true})),h(FormActions,null,h('button',{type:'submit'},'Save'))));
 assert.match(html,/<summary>Filters<\/summary>/);assert.match(html,/required/);assert.match(html,/type="submit"/);
 assert.equal((html.match(/<button/g)||[]).length,1);
});
