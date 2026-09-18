"""Shared low-level MIPS/patch-record primitives -- word packing, jump/branch encoding, and the Patch record every patches/*.py plan builder produces."""
import struct
from dataclasses import dataclass


def packed(*words: int) -> bytes:
    return struct.pack(f"<{len(words)}I", *words)


def jump(address: int) -> int:
    return 0x0C000000 | (address >> 2)


def j(address: int) -> int:
    """Plain (non-linking) MIPS J -- jump() above always emits JAL."""
    return 0x08000000 | (address >> 2)


def branch(source: int, target: int) -> int:
    displacement = (target - source - 4) // 4
    if source % 4 or target % 4 or not -32768 <= displacement <= 32767:
        raise ValueError("Invalid native branch")
    return 0x10000000 | (displacement & 0xFFFF)


@dataclass(frozen=True)
class Patch:
    address: int
    original: bytes
    replacement: bytes
