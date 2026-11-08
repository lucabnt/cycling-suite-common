import test from 'node:test';
import assert from 'node:assert/strict';
import {acquireBodyScrollLock} from '../packages/ui/dist/dialogScrollLock.js';

test('closing editor and nested confirmation together never leaves the page locked',()=>{
 for(const order of [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]]){
  const body={style:{overflow:'auto'}};
  const release=Array.from({length:3},()=>acquireBodyScrollLock(body));
  for(const index of order.slice(0,-1)){release[index]();assert.equal(body.style.overflow,'hidden')}
  release[order.at(-1)]();assert.equal(body.style.overflow,'auto');
 }
});

test('canceling a nested confirmation keeps the editor locked until its own close',()=>{
 const body={style:{overflow:''}};
 const editor=acquireBodyScrollLock(body),confirmation=acquireBodyScrollLock(body);
 confirmation();assert.equal(body.style.overflow,'hidden');
 editor();assert.equal(body.style.overflow,'');
});

test('effect replay and repeated release do not unlock another active dialog',()=>{
 const body={style:{overflow:'scroll'}};
 const first=acquireBodyScrollLock(body);first();first();
 const editor=acquireBodyScrollLock(body),confirmation=acquireBodyScrollLock(body);
 editor();editor();assert.equal(body.style.overflow,'hidden');
 confirmation();assert.equal(body.style.overflow,'scroll');
 const next=acquireBodyScrollLock(body);next();assert.equal(body.style.overflow,'scroll');
});

test('different documents and an initially hidden body retain their original styles',()=>{
 const a={style:{overflow:'hidden'}},b={style:{overflow:'auto'}};
 const releaseA=acquireBodyScrollLock(a),releaseB=acquireBodyScrollLock(b);
 releaseA();assert.equal(a.style.overflow,'hidden');assert.equal(b.style.overflow,'hidden');
 releaseB();assert.equal(b.style.overflow,'auto');
});
