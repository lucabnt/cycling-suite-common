import {useEffect,useRef,useState,type ReactNode} from 'react';

export type DialogProps={title:string;children:ReactNode;onClose:()=>void;wide?:boolean;editor?:boolean;busy?:boolean;locale?:'it'|'en';fullscreen?:boolean};

/** Native modal semantics keep focus, inert background and stacking consistent across products. */
export function Dialog({title,children,onClose,wide=true,editor=false,busy=false,locale='it',fullscreen=false}:DialogProps){
 const ref=useRef<HTMLDialogElement>(null),dirty=useRef(false);
 const [prompt,setPrompt]=useState(false);
 const close=()=>{if(busy)return;if(editor&&dirty.current)setPrompt(true);else onClose()};
 const callback=useRef(close);callback.current=close;
 useEffect(()=>{
  const dialog=ref.current!;
  const previous=document.activeElement as HTMLElement|null;
  const overflow=document.body.style.overflow;
  document.body.style.overflow='hidden';dialog.showModal();
  dialog.querySelector<HTMLButtonElement>('.suite-dialog-close')?.focus({preventScroll:true});
  dialog.scrollTop=0;
  return()=>{dialog.close();document.body.style.overflow=overflow;if(previous?.isConnected)previous.focus({preventScroll:true})};
 },[]);
 useEffect(()=>{
  const dialog=ref.current!;
  if(!document.documentElement.classList.contains('android'))return;
  const keyboards=()=>dialog.querySelectorAll<HTMLInputElement>('input[type=number]').forEach(input=>{
   if(!input.hasAttribute('inputmode')&&input.min!==''&&Number(input.min)>=0)input.inputMode=input.step==='any'||Number(input.step)<1?'decimal':'numeric';
  });
  keyboards();const observer=new MutationObserver(keyboards);observer.observe(dialog,{childList:true,subtree:true});
  const invalid=(event:Event)=>{const input=event.target as HTMLElement;requestAnimationFrame(()=>input.scrollIntoView({block:'center',behavior:'smooth'}))};
  dialog.addEventListener('invalid',invalid,true);
  return()=>{observer.disconnect();dialog.removeEventListener('invalid',invalid,true)};
 },[]);
 const en=locale==='en';
 return <dialog ref={ref} role="dialog" aria-modal="true" aria-label={title} className={'dialog suite-dialog'+(wide?' wide':'')+(fullscreen?' suite-dialog-fullscreen':'')}
  onCancel={e=>{e.preventDefault();e.stopPropagation();callback.current()}}
  onInputCapture={()=>{dirty.current=true}} onChangeCapture={()=>{dirty.current=true}}
  onClickCapture={e=>{const target=e.target as HTMLElement;if(target.closest('button')&&!target.closest('.suite-dialog-toolbar,.suite-discard-prompt'))dirty.current=true}}>
  <div className="suite-dialog-toolbar"><strong>{title}</strong><button className="suite-dialog-close" type="button" disabled={busy} aria-label={en?'Close dialog':'Chiudi finestra'} onClick={close}>×</button></div>
  {prompt&&<div className="hint suite-discard-prompt" role="alert"><p>{en?'Close and discard unsaved changes?':'Chiudere e perdere le modifiche non salvate?'}</p><div className="actions"><button type="button" onClick={()=>setPrompt(false)}>{en?'Continue editing':'Continua a modificare'}</button><button type="button" disabled={busy} onClick={onClose}>{en?'Discard and close':'Scarta e chiudi'}</button></div></div>}
  {children}
 </dialog>;
}
