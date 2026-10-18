import type {ReactNode} from 'react';

/** Label wrapper: pass id when using htmlFor, otherwise nest the input. */
export function Field({label,children,htmlFor}: {label:ReactNode;children:ReactNode;htmlFor?:string}) {
  return <label className="field" htmlFor={htmlFor}><span>{label}</span>{children}</label>;
}
