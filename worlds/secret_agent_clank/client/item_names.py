"""Translate historical AP equipment names at the client boundary only."""
from ..constants.weapons import EQUIPMENT_INTERNAL_TO_DISPLAY
from ..constants.weapon_progression import UNLOCK_TO_PROGRESSIVE


def _legacy_equipment_names() -> dict[str, str]:
    aliases: dict[str, str] = {}

    def add_unlock(suffix: str, display: str) -> None:
        aliases[f"Unlock: {suffix}"] = display
        if display in UNLOCK_TO_PROGRESSIVE:
            aliases[f"Progressive: {suffix}"] = UNLOCK_TO_PROGRESSIVE[display]

    # Earlier seeds classified several Clank tools as Ratchet unlocks.
    for internal, display in EQUIPMENT_INTERNAL_TO_DISPLAY.items():
        for character in ("Ratchet", "Clank"):
            add_unlock(f"{character} {internal}", display)

    for old, internal in (
        ("Kick Blast (Ratchet)", "kickblast"),
        ("Agency PDA (Ratchet)", "ratchetpda"),
        ("Bolt Transfer (Ratchet)", "bolttransfer"),
    ):
        aliases[old] = EQUIPMENT_INTERNAL_TO_DISPLAY[internal]

    for old, internal in (
        ("Bowtie", "throwTie"),
        ("Cufflink", "CuffLink"),
        ("Tanglevine", "TangleVine"),
        ("Flamethrower Briefcase", "FlamethrowerPen"),
        ("HoloKnuckles", "HoloKnuckles"),
        ("PDA", "clankpda"),
    ):
        add_unlock(f"Clank {old}", EQUIPMENT_INTERNAL_TO_DISPLAY[internal])
    return aliases


LEGACY_EQUIPMENT_NAMES = _legacy_equipment_names()


def canonical_item_name(server_name: str) -> str:
    return LEGACY_EQUIPMENT_NAMES.get(server_name, server_name)
