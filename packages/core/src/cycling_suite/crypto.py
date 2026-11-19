"""Cryptographic primitives shared by the suite apps (core 0.2.0).

Primitives only. Each product keeps its own formats, magic bytes, KDF
parameters, signature namespaces, error messages and compatibility readers.
The functions reproduce byte for byte the formats already delivered by
Fuorigiri (invitations/recovery) and Ammiraglia (vault, signed envelopes):
see tests/vectors in cycling-suite-common.

``cryptography`` is a dependency of every consumer app; it is imported here
and not declared by the wheel, like Qt for ``desktop``.
"""

import base64
import hmac
import json
import os
from dataclasses import dataclass

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

from .canonical import canonical, digest  # noqa: F401  (re-exported)

NONCE = 12
SALT = 16


def b64(raw):
    return base64.b64encode(raw).decode()


def un64(text):
    return base64.b64decode(text, validate=True)


# Ed25519 with raw 32-byte keys transported as standard base64.


def new_private_key():
    return b64(Ed25519PrivateKey.generate().private_bytes_raw())


def public_key(private):
    return b64(Ed25519PrivateKey.from_private_bytes(un64(private)).public_key().public_bytes_raw())


def sign(private, message):
    return b64(Ed25519PrivateKey.from_private_bytes(un64(private)).sign(message))


def verify(public, message, signature):
    """Raise ``cryptography.exceptions.InvalidSignature`` (or ValueError for bad encodings)."""
    Ed25519PublicKey.from_public_bytes(un64(public)).verify(un64(signature), message)


def sign_value(private, value):
    return sign(private, canonical(value).encode())


def verify_value(public, value, signature):
    verify(public, canonical(value).encode(), signature)


def derived_seed(secret, *parts):
    """Domain-separated HMAC-SHA256 seed; callers choose a unique first part."""
    return b64(hmac.digest(un64(secret), canonical(list(parts)).encode(), 'sha256'))


# scrypt


@dataclass(frozen=True)
class ScryptParams:
    n: int
    r: int = 8
    p: int = 1

    def as_dict(self):
        return {'name': 'scrypt', 'n': self.n, 'r': self.r, 'p': self.p}


def derive_key(password, salt, params, length=32):
    return Scrypt(salt=salt, length=length, n=params.n, r=params.r, p=params.p).derive(password.encode())


def bounded_scrypt(kdf, message, *, n_min=2**14, n_max=2**20, r=8, p=1):
    """Validate untrusted parameters so a crafted file cannot demand huge memory."""
    if (
        not isinstance(kdf, dict)
        or kdf.get('name') != 'scrypt'
        or type(kdf.get('n')) is not int
        or not n_min <= kdf['n'] <= n_max
        or kdf['n'] & (kdf['n'] - 1)
        or kdf.get('r') != r
        or kdf.get('p') != p
    ):
        raise ValueError(message)
    return ScryptParams(kdf['n'], r, p)


# JSON envelope: scrypt + Fernet, parameters stated in the envelope.


def seal_json(payload, password, params):
    salt = os.urandom(SALT)
    key = derive_key(password, salt, params)
    return canonical(
        {
            'kdf': params.as_dict(),
            'salt': b64(salt),
            'encrypted': Fernet(base64.urlsafe_b64encode(key)).encrypt(canonical(payload).encode()).decode(),
        }
    ).encode()


def unseal_json(raw, password, *, legacy, unsupported, invalid='Formato cifrato non valido.'):
    """Open a JSON envelope; envelopes without ``kdf`` use ``legacy`` parameters.

    Raises ``cryptography.fernet.InvalidToken`` for a wrong password.
    """
    envelope = json.loads(raw)
    salt = un64(envelope['salt'])
    if len(salt) != SALT:
        raise ValueError(invalid)
    params = bounded_scrypt(envelope.get('kdf', legacy.as_dict()), unsupported)
    key = derive_key(password, salt, params)
    return json.loads(Fernet(base64.urlsafe_b64encode(key)).decrypt(envelope['encrypted'].encode()))


# Binary AEAD frame: prefix || nonce || AES-GCM(ciphertext), whole header as AAD.


def aead_seal(raw, secret, prefix):
    nonce = os.urandom(NONCE)
    header = prefix + nonce
    return header + AESGCM(secret).encrypt(nonce, raw, header)


def aead_open(raw, secret, header_length):
    """Raise ``cryptography.exceptions.InvalidTag`` for a wrong key or altered data."""
    header = raw[:header_length]
    return AESGCM(secret).decrypt(header[-NONCE:], raw[header_length:], header)
