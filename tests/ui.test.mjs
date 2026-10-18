import test from 'node:test';
import assert from 'node:assert/strict';
import {createElement as h} from 'react';
import {renderToStaticMarkup as render} from 'react-dom/server';
import {readFile} from 'node:fs/promises';
import {compareValues,compareCellText,DataTable,SortableTable,Field,SuiteBranding,attribution} from '../packages/ui/dist/index.js';

test('numeric order and missing values remain distinct in both directions',()=>{
 for(const ascending of [true,false]){
  const result=[null,10,0,2,undefined].sort((a,b)=>compareValues(a,b,ascending));
  assert.deepEqual(result.slice(0,3),ascending?[0,2,10]:[10,2,0]);
  assert.equal(compareValues(null,0,ascending),1);
  assert.equal(compareCellText('—','0 W',ascending),1);
 }
 assert.ok(compareCellText('9,5 W','100 W')<0);
});
test('table controls cannot submit a surrounding data-entry form',()=>{
 const html=render(h(DataTable,{rows:[{id:'a',value:0},{id:'b',value:null},{id:'c',value:false}],columns:[{key:'value',label:'Dato'}]}));
 assert.match(html,/>0<\/td>/);assert.match(html,/>—<\/td>/);assert.match(html,/>false<\/td>/);
 assert.match(html,/<button type="button"/);assert.match(html,/aria-sort="none"/);
 const table=render(h(SortableTable,null,h('thead',null,h('tr',null,h('th',null,'Titolo'))),h('tbody',null)));
 assert.match(table,/<button type="button"/);
});
test('fixed society branding and local logo work for either product',async()=>{
 for(const productName of ['Fuorigiri Performance Lab','Ammiraglia']){
  const html=render(h(SuiteBranding,{productName}));
  assert.ok(html.includes(attribution));assert.ok(html.includes(productName+' · GPL'));
  assert.ok(html.includes('progetto-ciclismo.png'));assert.ok(html.includes('alt="Progetto Ciclismo'));
 }
 const png=await readFile(new URL('../packages/ui/dist/assets/progetto-ciclismo.png',import.meta.url));
 assert.equal(png.subarray(1,4).toString(),'PNG');
});
test('field label preserves accessible association and escapes text',()=>{
 const html=render(h(Field,{label:'Nome <atleta>',htmlFor:'name'},h('input',{id:'name'})));
 assert.match(html,/for="name"/);assert.match(html,/Nome &lt;atleta&gt;/);
});
