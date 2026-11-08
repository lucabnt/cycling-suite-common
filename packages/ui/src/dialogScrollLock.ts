type ScrollBody={style:{overflow:string}};
const locks=new WeakMap<ScrollBody,{count:number;overflow:string}>();

/** Restore the initial style only after the last dialog, regardless of teardown order. */
export function acquireBodyScrollLock(body:ScrollBody){
 const lock=locks.get(body)??{count:0,overflow:body.style.overflow};
 locks.set(body,lock);lock.count++;
 body.style.overflow='hidden';
 let released=false;
 return ()=>{
  if(released)return;
  released=true;
  if(--lock.count===0){body.style.overflow=lock.overflow;locks.delete(body)}
 };
}
