import React,{useState,type ReactNode,type ReactElement} from 'react';
import {compareValues,compareCellText} from './sorting.js';

export type DataRow=Record<string,any>;
export type Column={key:string;label:string;render?:(row:DataRow)=>ReactNode};

function cellText(node:any):string {
  if(node==null||typeof node==='boolean')return '';
  if(typeof node==='string'||typeof node==='number')return String(node);
  if(Array.isArray(node))return node.map(cellText).join(' ');
  return cellText(node.props?.children);
}

/** Compatibility component for existing declarative Fuorigiri tables. */
export function SortableTable({children}:{children:ReactNode}) {
  const [sort,setSort]=useState(-1),[ascending,setAscending]=useState(true);
  const sections=React.Children.toArray(children) as ReactElement<any>[];
  return <div className="table-scroll"><table>{sections.map(section=>{
    if(section.type==='thead')return React.cloneElement(section,{children:React.Children.map(section.props.children,(row:any)=>React.cloneElement(row,{children:React.Children.map(row.props.children,(cell:any,i)=>cellText(cell).trim()?React.cloneElement(cell,{'aria-sort':sort===i?(ascending?'ascending':'descending'):'none',children:<button type="button" onClick={()=>{setAscending(sort===i?!ascending:true);setSort(i)}}>{cell.props.children}{sort===i?(ascending?' ↑':' ↓'):''}</button>}):cell)}))});
    if(section.type==='tbody'&&sort>=0)return React.cloneElement(section,{children:(React.Children.toArray(section.props.children) as any[]).sort((a,b)=>compareCellText(cellText(React.Children.toArray(a.props.children)[sort]).trim(),cellText(React.Children.toArray(b.props.children)[sort]).trim(),ascending))});
    return section;
  })}</table></div>;
}

/** Sort raw values, not formatted labels. Null is distinct from zero and false. */
export function DataTable({rows,columns}:{rows:DataRow[];columns:Column[]}) {
  const [sort,setSort]=useState(''),[ascending,setAscending]=useState(true);
  const ordered=sort?[...rows].sort((a,b)=>compareValues(a[sort],b[sort],ascending)):rows;
  return <div className="table-scroll"><table><thead><tr>{columns.map(c=><th key={c.key} aria-sort={sort===c.key?(ascending?'ascending':'descending'):'none'}><button type="button" onClick={()=>{setAscending(sort===c.key?!ascending:true);setSort(c.key)}}>{c.label}{sort===c.key?(ascending?' ↑':' ↓'):''}</button></th>)}</tr></thead><tbody>{ordered.map((r,i)=><tr key={r.id||i}>{columns.map(c=><td key={c.key}>{c.render?c.render(r):typeof r[c.key]==='boolean'?String(r[c.key]):r[c.key]??'—'}</td>)}</tr>)}</tbody></table></div>;
}
