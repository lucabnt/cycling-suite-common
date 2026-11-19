"""Exchange invariants shared by the suite sync engines (core 0.2.0).

The engines, packet formats, signatures, access models and namespaces stay in
each app. These helpers carry the rules both engines apply in the same way:

- signed control documents (access lists, revocations, policy chains) are
  immutable per version: two different documents with the same version are a
  fork and fail closed;
- event packets are content-addressed by event id; an ordinary exchange skips
  ids already in the local journal, a full verification reads them all again;
- an immutable publication that collides with an existing object is accepted
  only when the app confirms the existing object carries the same signed
  content (ciphertexts differ for every encryption).
"""

from .canonical import canonical


def add_version(versions, number, document, fork):
    """Record ``document`` as version ``number``; ``fork()`` builds the error for a divergent copy."""
    previous = versions.get(number)
    if previous is not None and canonical(previous) != canonical(document):
        raise fork()
    versions[number] = document
    return versions


def event_names(names, suffix):
    """Map event id -> object name for the objects with ``suffix``."""
    return {name[: -len(suffix)]: name for name in names if name.endswith(suffix) and len(name) > len(suffix)}


def incremental(names, suffix, known, verify_all):
    """Return ``(to_read, skipped)``: (id, name) pairs to download in name order."""
    to_read = []
    skipped = 0
    for id, name in sorted(event_names(names, suffix).items(), key=lambda item: item[1]):
        if not verify_all and id in known:
            skipped += 1
            continue
        to_read.append((id, name))
    return to_read, skipped


def publish_immutable(transport, name, body, same_content):
    """Publish once; True when created, False when an equivalent object already exists.

    ``same_content(raw)`` receives the existing bytes and must return True only
    after authenticating them. Any other collision re-raises the transport error.
    """
    try:
        return bool(transport.put(name, body))
    except ValueError:
        if same_content(transport.get(name)):
            return False
        raise
