"""Every location in Venantonio Labs, each carrying its planet, case and access rule."""
from rule_builder.rules import Has, HasAll, True_

from ..constants import (
    SACAlienCodeLocations,
    SACCases,
    SACClankGadgets,
    SACClankWeapons,
    SACCutsceneLocations,
    SACMissionLocations,
    SACPickups,
    SACPlanets,
    SACSkillPointLocations,
    SACTitaniumBoltLocations,
)
from .model import SACLocation, SACLocationType

_PLANET = SACPlanets.VENANTONIO
_CASE = SACCases.VENANTONIO_LABS

_BASE = HasAll(SACClankWeapons.CUFFLINK, SACClankGadgets.OMNIKEY)
_BRIEFCASE_PATH = HasAll(SACClankWeapons.FLAMETHROWERPEN, SACClankWeapons.CUFFLINK)
_FINISH = _BRIEFCASE_PATH & Has(SACClankGadgets.OMNIKEY)

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACPickups.VENANTONIO_LABS_BLOWTORCH_BRIEFCASE,
        _PLANET,
        _CASE,
        SACLocationType.CLANK_WEAPON,
        77_815_002,
        lambda world: _BASE,
    ),
    SACLocation(
        SACTitaniumBoltLocations.VENANTONIO_LABS_1,
        _PLANET,
        _CASE,
        SACLocationType.TITANIUM_BOLT,
        77_815_901,
        lambda world: _BASE,
    ),
    SACLocation(
        SACTitaniumBoltLocations.VENANTONIO_LABS_2,
        _PLANET,
        _CASE,
        SACLocationType.TITANIUM_BOLT,
        77_815_902,
        lambda world: _BRIEFCASE_PATH,
    ),
    SACLocation(
        SACMissionLocations.VENANTONIO_LABS_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_815_004,
        lambda world: _FINISH,
    ),
    SACLocation(
        SACMissionLocations.VENANTONIO_LABS_CRASHING_THE_PARTY,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_815_005,
        lambda world: _BASE,
    ),
    SACLocation(
        SACMissionLocations.VENANTONIO_LABS_OUT_OF_THE_FRYING_PAN,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_815_006,
        lambda world: _FINISH,
    ),
    SACLocation(
        SACSkillPointLocations.VENANTONIO_LABS_ALL_SLIME_MUST_BURN,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_815_010,
        lambda world: _BASE & Has(SACClankWeapons.FLAMETHROWERPEN),
    ),
    SACLocation(
        SACSkillPointLocations.VENANTONIO_LABS_RAMMING_SPEED,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_815_011,
        lambda world: _BRIEFCASE_PATH,
    ),
    SACLocation(
        SACCutsceneLocations.VENANTONIO_LABS_ENTER_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_815_007,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.VENANTONIO_LABS_OPEN_GREEN_DOOR_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_815_008,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.VENANTONIO_LABS_COMPLETE_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_815_009,
        lambda world: _FINISH,
    ),
    SACLocation(
        SACAlienCodeLocations.VENANTONIO_LABS_GERARDS_SECRET,
        _PLANET,
        _CASE,
        SACLocationType.ALIEN_CODE,
        77_815_012,
        lambda world: Has(SACClankGadgets.THERM_OPTIC_SHADES),
    ),
    SACLocation(
        SACAlienCodeLocations.VENANTONIO_LABS_ALEXS_SECRET,
        _PLANET,
        _CASE,
        SACLocationType.ALIEN_CODE,
        77_815_013,
        lambda world: _BRIEFCASE_PATH & Has(SACClankGadgets.THERM_OPTIC_SHADES),
    ),
    SACLocation(
        SACAlienCodeLocations.VENANTONIO_LABS_HAROONS_SECRET,
        _PLANET,
        _CASE,
        SACLocationType.ALIEN_CODE,
        77_815_014,
        lambda world: _BRIEFCASE_PATH & Has(SACClankGadgets.THERM_OPTIC_SHADES),
    ),
)
