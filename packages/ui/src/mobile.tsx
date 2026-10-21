import {useState,type ReactNode} from 'react';

export type RecordCard={id:string;title:string;subtitle?:ReactNode;details:{label:string;value:ReactNode}[];badge?:ReactNode};
/** Compact, paged records: product supplies labels and values, never raw database columns. */
export function RecordCards({items,onOpen,actionLabel,locale='it',pageSize=20,resetKey='',pageIndex,onPageChange}:{items:RecordCard[];onOpen:(id:string)=>void;actionLabel:string;locale?:'it'|'en';pageSize?:number;resetKey?:string;pageIndex?:number;onPageChange?:(page:number)=>void}){
 const [position,setPosition]=useState({key:resetKey,page:0});
 const size=Math.max(1,Math.floor(pageSize));
 const last=Math.max(0,Math.ceil(items.length/size)-1);
 const page=Math.max(0,Math.min(pageIndex??(position.key===resetKey?position.page:0),last));
 const move=(next:number)=>{setPosition({key:resetKey,page:next});onPageChange?.(next)};
 const en=locale==='en';
 return <div className="suite-records"><ul className="suite-record-list">{items.slice(page*size,(page+1)*size).map(item=><li key={item.id}><article className="suite-record-card"><h3><button type="button" onClick={()=>onOpen(item.id)}>{item.title}</button></h3>{item.subtitle&&<p>{item.subtitle}</p>}{item.badge}<dl>{item.details.map((d,i)=><div key={i}><dt>{d.label}</dt><dd>{d.value}</dd></div>)}</dl><button type="button" onClick={()=>onOpen(item.id)} aria-label={actionLabel+' · '+item.title}>{actionLabel}</button></article></li>)}</ul>{items.length>size&&<div className="suite-pagination" aria-label={en?'List pages':'Pagine elenco'}><button type="button" disabled={page===0} onClick={()=>move(page-1)}>{en?'Previous':'Precedenti'}</button><span role="status">{page*size+1}–{Math.min((page+1)*size,items.length)} / {items.length}</span><button type="button" disabled={page===last} onClick={()=>move(page+1)}>{en?'Next':'Successivi'}</button></div>}</div>;
}
export function CollapsibleFilters({label,children}:{label:string;children:ReactNode}){return <details className="suite-filters"><summary>{label}</summary><div className="form-grid">{children}</div></details>}
/** Sticky within the editor scrollport; always uses the original buttons and form validation. */
export function FormActions({children}:{children:ReactNode}){return <div className="suite-form-actions">{children}</div>}

/** Product supplies truthful phase/error text; no fictitious progress percentage. */
export function LoadingState({title,detail,retry,retryLabel}:{title:string;detail:string;retry?:()=>void;retryLabel?:string}){
 return <section className="suite-loading" aria-label={title}><div role={retry?'alert':'status'} aria-live="polite">{!retry&&<span className="suite-spinner" aria-hidden="true"/>}<h2>{title}</h2><p>{detail}</p></div>{retry&&<button type="button" onClick={retry}>{retryLabel}</button>}</section>;
}
/** Reusable chart surface; data, touch modes and scientific meaning belong to the app. */
export function ChartFrame({label,tools,children,wide=false,toolsAfter=false,fullscreen=false}:{label:string;tools?:ReactNode;children:ReactNode;wide?:boolean;toolsAfter?:boolean;fullscreen?:boolean}){
 return <section className={'suite-chart'+(wide?' suite-chart-wide':'')+(fullscreen?' suite-chart-fullscreen':'')} aria-label={label}>{!toolsAfter&&tools&&<div className="suite-chart-tools" role="group" aria-label={label}>{tools}</div>}{children}{toolsAfter&&tools&&<div className="suite-chart-tools" role="group" aria-label={label}>{tools}</div>}</section>;
}

/** Optional chart/tools panel: product owns commands and data. */
export function FloatingPanel({label,children}:{label:string;children:ReactNode}){return <details className="suite-floating-panel"><summary>{label}</summary><div>{children}</div></details>}
