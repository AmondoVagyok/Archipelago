"""SACLocation: one record per AP location, with its planet, case, category and access rule."""
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING

from ..constants.skill_point_requirements import SKILL_POINT_REQUIREMENTS
from ..constants.vendor import NG_PLUS_VENDOR_ITEMS
from ..options import Missions

if TYPE_CHECKING:
    from rule_builder.rules import Rule

    from ..options import SecretAgentClankOptions
    from ..world import SecretAgentClankWorld

BASE_ID = 77_800_000


class SACLocationType(Enum):
    RATCHET_WEAPON = auto()
    CLANK_WEAPON = auto()
    CLANK_GADGET = auto()
    GADGET_PICKUP = auto()
    GADGETBOT_CHALLENGE = auto()
    SPECIAL_CHALLENGE = auto()
    RATCHET_CHALLENGE = auto()
    TITANIUM_BOLT = auto()
    CASE_COMPLETE = auto()
    MISSION = auto()
    SKILL_POINT = auto()
    CUTSCENE = auto()
    KEYCARD = auto()
    ALIEN_CODE = auto()
    VENDOR = auto()
    TITAN_VENDOR = auto()
    MOD_VENDOR = auto()
    WEAPON_LEVEL = auto()
    NANOTECH = auto()
    STEALTH_TAKEDOWN = auto()


# Order of location types within a case region: pickups first, then missions and
# each optional category.
_REGION_TYPE_ORDER: tuple[SACLocationType, ...] = (
    SACLocationType.RATCHET_WEAPON, SACLocationType.CLANK_WEAPON, SACLocationType.CLANK_GADGET,
    SACLocationType.GADGET_PICKUP, SACLocationType.GADGETBOT_CHALLENGE, SACLocationType.SPECIAL_CHALLENGE,
    SACLocationType.RATCHET_CHALLENGE, SACLocationType.TITANIUM_BOLT, SACLocationType.CASE_COMPLETE,
    SACLocationType.MISSION, SACLocationType.SKILL_POINT, SACLocationType.CUTSCENE,
    SACLocationType.KEYCARD, SACLocationType.ALIEN_CODE,
)


@dataclass(frozen=True, slots=True)
class SACLocation:
    name: str
    planet: str | None  # SACPlanets constant; None only for the vendor-catalog regions.
    case: str | None    # SACCases constant; None only for the vendor-catalog regions.
    type: SACLocationType
    code: int
    # Called with the world in set_rules; None means reachable with the case region.
    rule: "Callable[[SecretAgentClankWorld], Rule] | None" = None

    def available(self, options: "SecretAgentClankOptions") -> bool:
        """Whether this location exists at all under the given options (the category toggles)."""
        match self.type:
            case SACLocationType.VENDOR:
                return self.name.removeprefix("Vendor: ") not in NG_PLUS_VENDOR_ITEMS or bool(options.ng_plus.value)
            case SACLocationType.CASE_COMPLETE:
                return options.all_missions.value != Missions.option_all
            case SACLocationType.MISSION:
                return options.all_missions.value == Missions.option_all
            case SACLocationType.SKILL_POINT:
                requirement = SKILL_POINT_REQUIREMENTS[self.name]
                return (options.skill_points.value >= requirement.difficulty
                        and all(options.operatives.value.get(operative, 0)
                                for operative in requirement.operatives))
            case SACLocationType.CUTSCENE:
                return bool(options.all_cutscenes)
            case SACLocationType.KEYCARD:
                return bool(options.all_keycards)
            case SACLocationType.ALIEN_CODE:
                return bool(options.all_alien_codes)
        return True

    @property
    def region_order(self) -> int:
        return _REGION_TYPE_ORDER.index(self.type)
