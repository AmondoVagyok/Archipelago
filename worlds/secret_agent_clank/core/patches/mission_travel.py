"""Use the native end-of-level map instead of forced next-planet travel."""
from ..symbols import require
from .asm import Patch, branch, jump, packed


def prepare_mission_travel(pine, symbols):
    function, map_ender = require(symbols,
        'UPDATE_ChangeToLevelOrMapIfAlreadyCompleted__Fi', 'SCRNGALACTICMAP_SetLevelEnder__Fv',
    )
    if (pine.read_bytes(function, 12) != packed([0x27BDFFF0, 0xFFB00000, 0xFFBF0008])
            or pine.read_bytes(function + 0x14, 12) != packed([0x0050102B, 0x14400010, 0x0200202D])
            or pine.read_int32(function + 0x20) != jump(map_ender, True)
            or pine.read_int32(function + 0x34) != 0x2404000E):
        raise RuntimeError('Mission-end travel layout changed')
    # Only bypass the choice of forced travel, preserving the existing map
    # opening path, completion processing and manual Case Files travel code.
    edits = [Patch(function + 0x18, packed([0x14400010]), packed([0]))]
    # Ratchet's results screen bypasses the generic completion helper. Its
    # Continue row has two routes: straight to the next level, or a movie
    # whose completion callback loads it. Redirect both, leaving challenge
    # selection, quitting and the Case Files launch handler alone.
    update, exit_screen, next_level, set_next, change = require(symbols,
        'SCRNRATCHETARENA_Update__Fv', 'SCRNRATCHETARENA_Exit__Fv', 'Arena_GetLevelToLoad__Fv',
        'SetNextLevel__Fi', 'UPDATE_ChangeToLevel__Fib',
    )
    direct = update + 0x188
    callback = exit_screen + 0x38
    if (pine.read_bytes(direct, 16) != packed([
            jump(next_level, True), 0, 0x10000014, 0x0040202D])
            or pine.read_int32(update + 0x228) != 0x1240000B
            or pine.read_bytes(callback, 24) != packed([
                0x27BDFFF0, 0xFFBF0000, jump(next_level, True), 0,
                jump(set_next, True), 0x0040202D])
            or pine.read_int32(callback + 0x20) != jump(change, True)
            or pine.read_bytes(callback + 0x28, 12) != packed([
                0xDFBF0000, 0x03E00008, 0x27BD0010])):
        raise RuntimeError('Ratchet completion travel layout changed')
    # Prove that the movie callback registered by the Continue row is the
    # same unnamed function we just validated after the exported Exit.
    hi = (callback + 0x8000) >> 16
    if (pine.read_int32(update + 0x158) != (0x3C060000 | hi)
            or pine.read_int32(update + 0x160) != (0x24C60000 | (callback & 0xFFFF))):
        raise RuntimeError('Ratchet completion movie callback changed')
    edits += [Patch(direct, pine.read_bytes(direct, 16), packed([
        jump(function, True), 0, branch(direct + 8, update + 0x228), 0])),
        Patch(callback + 0x20, packed([jump(change, True)]), packed([jump(function, True)]))]
    return edits
