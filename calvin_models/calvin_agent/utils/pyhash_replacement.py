from __future__ import annotations

from typing import Union

# FNV-1 32-bit parameters
_FNV32_OFFSET_BASIS = 2166136261
_FNV32_PRIME = 16777619
_MASK32 = 0xFFFFFFFF


def fnv1_32_hasher():
    """
    Returns a callable that computes FNV-1 32-bit hashes.

    Designed to replace:
        import pyhash
        hasher = pyhash.fnv1_32()
        h = hasher(data)

    Compatibility notes:
    - If `data` is `str`, we encode as UTF-8 (common in pyhash usage).
      If Calvin previously passed bytes, hashes will match exactly.
    - Always returns an unsigned 32-bit int.
    """

    def _hash(data: Union[bytes, bytearray, memoryview, str]) -> int:
        if isinstance(data, str):
            b = data.encode("utf-8")
        elif isinstance(data, (bytes, bytearray, memoryview)):
            b = bytes(data)
        else:
            # Match typical pyhash behavior: stringify then hash bytes
            b = str(data).encode("utf-8")

        h = _FNV32_OFFSET_BASIS
        for byte in b:
            h = (h * _FNV32_PRIME) & _MASK32
            h ^= byte
        return h

    return _hash
