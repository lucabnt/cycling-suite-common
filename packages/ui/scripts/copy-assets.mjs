import {cp,mkdir} from 'node:fs/promises';
const root=new URL('../',import.meta.url);
await mkdir(new URL('dist/assets/',root),{recursive:true});
for(const name of ['theme.css','components.css'])await cp(new URL('src/'+name,root),new URL('dist/'+name,root));
await cp(new URL('src/assets/progetto-ciclismo.png',root),new URL('dist/assets/progetto-ciclismo.png',root));
