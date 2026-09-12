"""Trap item effects -- force one or more vanilla cheats on for a duration
(see constants/cheats.py's TRAP_CHEATS).

TODO: CHEATS_ADDRESS's layout (see core/address_maps/ps2.py) is
unconfirmed -- one bit per cheat? Same list order as
constants/cheats.py's SACCheats? -- so this can't actually flip a cheat on
in game memory yet. activate_trap() logs the attempt so the item's effect
is at least visible/debuggable once wired up for real."""
import logging
from typing import TYPE_CHECKING

from ..constants.cheats import TRAP_CHEATS

if TYPE_CHECKING:
    from ..pypine import Pine

logger = logging.getLogger("CommonClient")


def activate_trap(pine: "Pine", trap_name: str) -> None:
    del pine  # unused until CHEATS_ADDRESS's layout is confirmed
    cheats = TRAP_CHEATS.get(trap_name, ())
    logger.warning(
        f"[SAC] {trap_name} received -- would enable {', '.join(cheats) or 'unknown cheat(s)'}, "
        "but CHEATS_ADDRESS's layout isn't confirmed yet, so nothing was written."
    )
