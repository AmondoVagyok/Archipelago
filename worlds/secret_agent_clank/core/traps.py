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
