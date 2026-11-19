# Origine e risorse

Codice originale estratto e adattato da Fuorigiri Performance Lab, Luca Bontempi, commit e1f01bc, ottobre 2026. Codice GPL-3.0-or-later; conservare questo avviso e LICENSE nelle distribuzioni.

Il logo `packages/ui/src/assets/progetto-ciclismo.png` è quello fornito per il software sviluppato per Progetto Ciclismo - Rodengo Saiano A.S.D.; è conservato senza modifiche. Il marchio è distinto dal codice GPL: la distribuzione del sorgente non concede automaticamente diritti ulteriori sul marchio.

React, TypeScript, Vite e gli altri strumenti mantengono le loro licenze. Il pacchetto UI dichiara React come peer dependency, senza includerne una seconda copia. La lista risolta delle dipendenze di sviluppo è in package-lock.json. Nessun font viene scaricato da CDN: il tema indica un insieme di font di sistema.
# Common Python runtime

The transport, credential-vault, archive-instance-lock and desktop-shell primitives
are derived from Fuorigiri Performance Lab, developed by Luca Bontempi for
Progetto Ciclismo - Rodengo Saiano A.S.D. Source: sibling repository `test-analysis`,
product sources 0.10.0, extracted on 20 October 2026. Distributed under
GPL-3.0-or-later; see LICENSE. The wheel contains the maintained Python source.
Product names, data, authorities, vault service names and compatibility adapters
remain the responsibility of each application. This package does not grant rights
to society marks or establish trust between archives.

Core 0.2.0 (19 November 2026) adds primitives derived from Fuorigiri and
Ammiraglia (`club-lab`): canonical JSON, Ed25519 helpers, scrypt/Fernet and
AES-GCM envelopes (`crypto`), atomic writes (`files`), CSV formula
neutralization (`csv_safety`), the fixed suite attribution (`branding`), job
runner and automatic exchange schedule (`jobs`) and exchange invariants
(`exchange`). Formats, magic bytes, KDF parameters, signature namespaces,
access models and sync engines remain in each application.
