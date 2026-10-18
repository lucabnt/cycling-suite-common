// Society branding is fixed. Only the consuming application's name varies.
export const attribution='Sviluppato da Luca Bontempi per Progetto CIclismo - Rodengo Saiano A.S.D.';
const societyUrl='https://www.asdprogettociclismorodengosaiano.it/';
const societyLogo=new URL('./assets/progetto-ciclismo.png',import.meta.url).href;

export function SuiteBranding({productName}:{productName:string}) {
  return <footer className="suite-footer"><a href={societyUrl} target="_blank" rel="noreferrer"><img src={societyLogo} alt="Progetto Ciclismo - Rodengo Saiano A.S.D."/></a><div>{attribution}<br/><a href="https://lucabontempi.com/" target="_blank" rel="noreferrer">Luca Bontempi</a> · <a href={societyUrl} target="_blank" rel="noreferrer">Progetto Ciclismo - Rodengo Saiano A.S.D.</a><br/>Strumenti aperti a supporto del ciclismo giovanile</div><span>{productName} · GPL</span></footer>;
}
