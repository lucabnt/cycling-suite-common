/** Explicit, reproducible delivery. Applications never depend on a sibling at runtime. */
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {copyFileSync, existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync} from 'node:fs';
import {resolve, dirname, basename} from 'node:path';
import {fileURLToPath} from 'node:url';

const root=resolve(dirname(fileURLToPath(import.meta.url)), '..');
const json=p=>JSON.parse(readFileSync(p,'utf8'));
const digest=(raw,algorithm='sha256',encoding='hex')=>createHash(algorithm).update(raw).digest(encoding);
export function sourceDigest(directory=resolve(root,'packages/ui')) {
  const hash=createHash('sha256');
  function visit(relative) {
    const path=resolve(directory,relative);
    for(const entry of readdirSync(path,{withFileTypes:true}).sort((a,b)=>a.name.localeCompare(b.name,'en'))) {
      const name=relative?relative+'/'+entry.name:entry.name;
      if(entry.isDirectory())visit(name);
      else {hash.update(name+'\0');hash.update(readFileSync(resolve(directory,name)));hash.update('\0');}
    }
  }
  for(const name of ['package.json','tsconfig.json','LICENSE','NOTICE.md','README.md']) {hash.update(name+'\0');hash.update(readFileSync(resolve(directory,name)));hash.update('\0');}
  visit('src');visit('scripts');return hash.digest('hex');
}
export function verifyCurrentDelivery(app) {
  const meta=verifyDelivery(app),pkg=json(resolve(root,'packages/ui/package.json'));
  if(meta.version!==pkg.version || meta.source_digest!==sourceDigest())throw new Error('UI comune superata: rigenerare con sync:ui e una nuova versione se già consegnata.');
  return meta;
}
function runNpm(args,cwd) {
  // npm's JS entry point avoids shell interpolation and Windows .cmd quoting.
  const cli=process.env.npm_execpath;
  if(!cli) throw new Error('Avviare con npm run sync:ui.');
  execFileSync(process.execPath,[cli,...args],{cwd,stdio:'inherit'});
}
export function verifyDelivery(app) {
  const vendor=resolve(app,'frontend/vendor');
  const meta=json(resolve(vendor,'suite-ui-provenance.json'));
  if(basename(meta.artifact)!==meta.artifact || !/^cycling-suite-ui-[\w.-]+\.tgz$/.test(meta.artifact)) throw new Error('Nome artefatto non valido.');
  const raw=readFileSync(resolve(vendor,meta.artifact));
  const pkg=json(resolve(app,'frontend/package.json'));
  const lock=json(resolve(app,'frontend/package-lock.json'));
  const spec='file:vendor/'+meta.artifact;
  const entry=lock.packages?.['node_modules/@cycling-suite/ui'];
  if(meta.package!=='@cycling-suite/ui' || digest(raw)!==meta.sha256 ||
     pkg.dependencies?.[meta.package]!==spec || lock.packages?.['']?.dependencies?.[meta.package]!==spec ||
     entry?.version!==meta.version || entry?.resolved!==spec ||
     entry?.integrity!=='sha512-'+digest(raw,'sha512','base64')) throw new Error('Artefatto, provenienza e lockfile UI non coerenti.');
  return meta;
}
function main() {
  const args=process.argv.slice(2),apps=[];let check=false;
  for(let i=0;i<args.length;i++) {
    if(args[i]==='--check')check=true;
    else if(args[i]==='--app' && args[i+1])apps.push(resolve(args[++i]));
    else throw new Error('Uso: npm run sync:ui -- --app ../club-lab [--app ../test-analysis] [--check]');
  }
  if(!apps.length)throw new Error('Specificare almeno una applicazione con --app.');
  for(const app of apps) {
    if(app===root || !existsSync(resolve(app,'frontend/package.json')))throw new Error('Frontend applicazione non trovato: '+app);
  }
  if(check) {
    for(const app of apps) {const m=verifyCurrentDelivery(app); console.log(`${app}: UI ${m.version} allineata alla sorgente comune (${m.sha256}).`);}
    return;
  }
  runNpm(['test'],root);
  runNpm(['run','pack:ui'],root);
  const pkg=json(resolve(root,'packages/ui/package.json'));
  const artifact=`cycling-suite-ui-${pkg.version}.tgz`;
  const raw=readFileSync(resolve(root,'artifacts',artifact));
  const source_revision=execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim();
  const source_dirty=Boolean(execFileSync('git',['status','--porcelain','--untracked-files=all'],{cwd:root,encoding:'utf8'}).trim());
  const meta={package:pkg.name,version:pkg.version,artifact,sha256:digest(raw),source_digest:sourceDigest(),source_repository:'cycling-suite-common',source_revision,source_dirty,license:pkg.license,contains_sources:true};
  // Prepare every target before mutation; no guessed paths or branch tracking.
  for(const app of apps) {
    const target=resolve(app,'frontend/vendor');mkdirSync(target,{recursive:true});
    const previous=existsSync(resolve(target,'suite-ui-provenance.json'))?json(resolve(target,'suite-ui-provenance.json')):null;
    if(previous?.version===pkg.version && previous?.sha256!==meta.sha256)throw new Error(`UI ${pkg.version} già consegnata con altri byte in ${app}: incrementare la versione.`);
  }
  for(const app of apps) {
    const target=resolve(app,'frontend/vendor');
    copyFileSync(resolve(root,'artifacts',artifact),resolve(target,artifact));
    runNpm(['install','./vendor/'+artifact,'--save-exact','--ignore-scripts','--no-audit','--no-fund'],resolve(app,'frontend'));
    const provenance=resolve(target,'suite-ui-provenance.json');
    // Byte-identical delivery retains the original immutable release provenance/tag.
    if(!existsSync(provenance) || json(provenance).sha256!==meta.sha256) {
      writeFileSync(provenance,JSON.stringify(meta,null,2)+'\n');
    }
    verifyDelivery(app);
    console.log(`UI ${pkg.version} consegnata e verificata in ${app}.`);
  }
}
if(process.argv[1] && resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
  try {main();} catch(error) {console.error(error.message);process.exitCode=1;}
}
