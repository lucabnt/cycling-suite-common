import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,mkdirSync,writeFileSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createHash} from 'node:crypto';
import {verifyDelivery,verifyCurrentDelivery,sourceDigest} from '../scripts/sync-ui.mjs';

test('delivery verifies actual tarball bytes, root dependency and lock integrity',()=>{
  const root=mkdtempSync(join(tmpdir(),'suite-delivery-'));
  try{
    const vendor=join(root,'frontend/vendor');mkdirSync(vendor,{recursive:true});
    const raw=Buffer.from('synthetic archive fixture');
    const artifact='cycling-suite-ui-0.1.0.tgz',name='@cycling-suite/ui',spec='file:vendor/'+artifact;
    const put=(path,data)=>writeFileSync(join(root,path),JSON.stringify(data));
    writeFileSync(join(vendor,artifact),raw);
    put('frontend/vendor/suite-ui-provenance.json',{package:name,version:'0.1.0',artifact,sha256:createHash('sha256').update(raw).digest('hex')});
    put('frontend/package.json',{dependencies:{[name]:spec}});
    const lock={packages:{'':{dependencies:{[name]:spec}},['node_modules/'+name]:{version:'0.1.0',resolved:spec,integrity:'sha512-'+createHash('sha512').update(raw).digest('base64')}}};
    put('frontend/package-lock.json',lock);
    assert.equal(verifyDelivery(root).version,'0.1.0');
    assert.throws(()=>verifyCurrentDelivery(root),/superata/);
    writeFileSync(join(vendor,artifact),'modified bytes');
    assert.throws(()=>verifyDelivery(root),/non coerenti/);
    writeFileSync(join(vendor,artifact),raw);
    lock.packages[''].dependencies[name]='file:../../common';put('frontend/package-lock.json',lock);
    assert.throws(()=>verifyDelivery(root),/non coerenti/);
    put('frontend/vendor/suite-ui-provenance.json',{artifact:'../escape.tgz'});
    assert.throws(()=>verifyDelivery(root),/non valido/);
  }finally{rmSync(root,{recursive:true,force:true})}
});


test('source fingerprint is deterministic and detects changed shared sources',()=>{
 const root=mkdtempSync(join(tmpdir(),'suite-source-'));
 try{
  for(const name of ['package.json','tsconfig.json','LICENSE','NOTICE.md','README.md'])writeFileSync(join(root,name),'fixture');
  mkdirSync(join(root,'src'));mkdirSync(join(root,'scripts'));
  writeFileSync(join(root,'src','index.ts'),'first');
  const before=sourceDigest(root);assert.equal(sourceDigest(root),before);
  writeFileSync(join(root,'src','index.ts'),'second');assert.notEqual(sourceDigest(root),before);
 }finally{rmSync(root,{recursive:true,force:true})}
});
