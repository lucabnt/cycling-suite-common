export function compareValues(a:unknown,b:unknown,ascending=true):number {
  // Missing values always sort last, including descending order. Zero is valid.
  if(a==null)return b==null?0:1;
  if(b==null)return -1;
  const result=typeof a==='number'&&typeof b==='number' ? a-b : String(a).localeCompare(String(b),undefined,{numeric:true});
  return ascending?result:-result;
}

export function compareCellText(a:string,b:string,ascending=true):number {
  const missing=(v:string)=>!v||v==='—'||v==='n.d.';
  if(missing(a))return missing(b)?0:1;
  if(missing(b))return -1;
  const numeric=(v:string)=>/^[-+]?\d+(?:[.,]\d+)?(?:\s*(?:W|kg|cm|bpm|W\/kg))?$/.test(v)?parseFloat(v.replace(',','.')):v;
  return compareValues(numeric(a),numeric(b),ascending);
}
