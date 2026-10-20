import {useEffect,useRef,useState} from 'react';
import {clock,parseClock} from './timeModel.js';
export {clock,parseClock} from './timeModel.js';
export function validTimes(target:HTMLElement){for(const input of target.closest('[role="dialog"]')?.querySelectorAll<HTMLInputElement>('.time-input input')||[]){if(!input.reportValidity())return false}return true}
export function TimeInput({label,value,onChange,locale='it'}:{label:string,value:number|string|null|undefined,onChange:(v:number|null)=>void,locale?:'it'|'en'}){
 const [text,setText]=useState(value==null||value===''?'':clock(Number(value)));const ref=useRef<HTMLInputElement>(null);
 useEffect(()=>{setText(value==null||value===''?'':clock(Number(value)));ref.current?.setCustomValidity('')},[value]);
 const invalid=!!text&&parseClock(text)==null;
 return <fieldset className="time-input"><legend>{label}</legend><label>{locale==='en'?'Seconds':'Secondi'}<input aria-label={label+' · s'} type="number" min="0" step="any" value={value??''} onChange={e=>onChange(e.target.value===''?null:Number(e.target.value))}/></label><label>mm:ss<input ref={ref} aria-label={label+' · mm:ss'} value={text} placeholder="23:45" aria-invalid={invalid} onChange={e=>{setText(e.target.value);const t=parseClock(e.target.value);e.target.setCustomValidity(e.target.value&&t==null?'Usa mm:ss (es. 23:45)':'');if(t!=null)onChange(t);else if(!e.target.value)onChange(null)}}/></label>{invalid&&<small role="alert">{locale==='en'?'Use minutes:seconds, e.g. 23:45.':'Usa minuti:secondi, per esempio 23:45.'}</small>}</fieldset>
}
