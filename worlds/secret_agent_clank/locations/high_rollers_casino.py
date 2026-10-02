"""Every location in High-Rollers Casino, each carrying its planet, case and access rule."""
from rule_builder.rules import Has, True_

from ..constants import (
    SACAlienCodeLocations,
    SACCases,
    SACClankGadgets,
    SACCutsceneLocations,
    SACMissionLocations,
    SACPlanets,
    SACSkillPointLocations,
    SACTitaniumBoltLocations,
)
from .model import SACLocation, SACLocationType

_PLANET = SACPlanets.CASINO
_CASE = SACCases.HIGH_ROLLERS_CASINO

_BASE = Has(SACClankGadgets.HOLOMONOCLE)

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACClankGadgets.HOLOMONOCLE,
        _PLANET,
        _CASE,
        SACLocationType.CLANK_GADGET,
        77_812_002,
        lambda world: True_(),
    ),
    SACLocation(
        SACTitaniumBoltLocations.HIGH_ROLLERS_CASINO_1,
        _PLANET,
        _CASE,
        SACLocationType.TITANIUM_BOLT,
        77_812_901,
        lambda world: _BASE & Has(SACClankGadgets.OMNIKEY),
    ),
    SACLocation(
        SACMissionLocations.HIGH_ROLLERS_CASINO_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_812_003,
        lambda world: _BASE,
    ),
    SACLocation(
        SACMissionLocations.HIGH_ROLLERS_CASINO_EXPLORE_PARADISE,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_812_004,
        lambda world: _BASE,
    ),
    SACLocation(
        SACMissionLocations.HIGH_ROLLERS_CASINO_PARADISE_EXPLOITED,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_812_005,
        lambda world: _BASE,
    ),
    SACLocation(
        SACSkillPointLocations.HIGH_ROLLERS_CASINO_BEAT_THE_HOUSE,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_812_008,
        lambda world: _BASE,
    ),
    SACLocation(
        SACCutsceneLocations.HIGH_ROLLERS_CASINO_ENTER_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_812_006,
        lambda world: _BASE,
    ),
    SACLocation(
        SACCutsceneLocations.HIGH_ROLLERS_CASINO_COMPLETE_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_812_007,
        lambda world: True_(),
    ),
    SACLocation(
        SACAlienCodeLocations.HIGH_ROLLERS_CASINO_COLINS_SECRET,
        _PLANET,
        _CASE,
        SACLocationType.ALIEN_CODE,
        77_812_009,
        lambda world: Has(SACClankGadgets.THERM_OPTIC_SHADES),
    ),
    SACLocation(
        SACAlienCodeLocations.HIGH_ROLLERS_CASINO_SHANES_SECRET,
        _PLANET,
        _CASE,
        SACLocationType.ALIEN_CODE,
        77_812_010,
        lambda world: _BASE & Has(SACClankGadgets.THERM_OPTIC_SHADES),
    ),
    SACLocation(
        SACAlienCodeLocations.HIGH_ROLLERS_CASINO_THE_PING_PONG_SECRET,
        _PLANET,
        _CASE,
        SACLocationType.ALIEN_CODE,
        77_812_011,
        lambda world: _BASE & Has(SACClankGadgets.THERM_OPTIC_SHADES),
    ),
)
