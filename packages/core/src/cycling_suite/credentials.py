"""Explicit OS credential backends; never fall back to a file or plaintext."""
import hashlib
import sys
from pathlib import Path

def account(root):
    return hashlib.sha256(str(Path(root).resolve()).encode()).hexdigest()

def backend():
    if sys.platform=='win32':
        from keyring.backends.Windows import WinVaultKeyring
        return WinVaultKeyring()
    from keyring.backends.SecretService import Keyring
    return Keyring()

class Secrets:
    def __init__(self,service,provider=None):
        if not isinstance(service,str) or not service.strip():raise ValueError('Servizio portachiavi obbligatorio.')
        self.service=service
        self.provider=provider or backend

    def read(self,key):
        try:return self.provider().get_password(self.service,key)
        except Exception:raise ValueError('Impossibile aprire il portachiavi di sistema.') from None

    def save(self,key,value):
        if not isinstance(value,str):raise ValueError('Segreto non valido.')
        try:self.provider().set_password(self.service,key,value)
        except Exception:raise ValueError('Portachiavi di sistema non disponibile o bloccato. Nessun fallback su file; sbloccare il portachiavi e riprovare.') from None

    def delete(self,key):
        try:
            vault=self.provider()
            if vault.get_password(self.service,key) is not None:vault.delete_password(self.service,key)
        except Exception:raise ValueError('Impossibile rimuovere il segreto dal portachiavi.') from None
