"""27 Alien Codes: three each in nine native modules."""
from dataclasses import dataclass


@dataclass(frozen=True)
class SACAlienCodeLocations:
    BOLTAIRE_MUSEUM_THE_LEGENDS = "Boltaire (Clank) - Boltaire Museum: Alien Code: The Legends"
    BOLTAIRE_MUSEUM_RONNS_SECRET = "Boltaire (Clank) - Boltaire Museum: Alien Code: Ronn's secret"
    BOLTAIRE_MUSEUM_BENS_SECRET = "Boltaire (Clank) - Boltaire Museum: Alien Code: Ben's secret"
    ASYANICA_ROOFTOPS_JHAIROS_SECRET = "Asyanica (Clank) - Asyanica Rooftops: Alien Code: Jhairo's secret"
    ASYANICA_ROOFTOPS_GILBERTS_SECRET = "Asyanica (Clank) - Asyanica Rooftops: Alien Code: Gilbert's secret"
    ASYANICA_ROOFTOPS_RICARDOS_SECRET = "Asyanica (Clank) - Asyanica Rooftops: Alien Code: Ricardo's secret"
    GONDOLA_ASCENT_LEVITICUS_SECRET = "Rionosis (Clank) - Gondola Ascent: Alien Code: Leviticus' secret"
    GONDOLA_ASCENT_CARLS_SECRET = "Rionosis (Clank) - Gondola Ascent: Alien Code: Carl's secret"
    GONDOLA_ASCENT_JESS_SECRET = "Rionosis (Clank) - Gondola Ascent: Alien Code: Jess' secret"
    AZCOTAL_ALLEY_JONS_SECRET = "Rionosis (Clank) - Azcotal Alley: Alien Code: Jon's secret"
    AZCOTAL_ALLEY_THE_3_JASONS_SECRET = "Rionosis (Clank) - Azcotal Alley: Alien Code: The 3 Jasons' secret"
    AZCOTAL_ALLEY_TRAVIS_SECRET = "Rionosis (Clank) - Azcotal Alley: Alien Code: Travis' secret"
    HIGH_ROLLERS_CASINO_COLINS_SECRET = "The Paradis Des Tricheurs Casino (Clank) - High-Rollers Casino: Alien Code: Colin's secret"
    HIGH_ROLLERS_CASINO_SHANES_SECRET = "The Paradis Des Tricheurs Casino (Clank) - High-Rollers Casino: Alien Code: Shane's secret"
    HIGH_ROLLERS_CASINO_THE_PING_PONG_SECRET = "The Paradis Des Tricheurs Casino (Clank) - High-Rollers Casino: Alien Code: The Ping Pong Secret"
    VENANTONIO_LABS_GERARDS_SECRET = "Venantonio (Clank) - Venantonio Labs: Alien Code: Gerard's secret"
    VENANTONIO_LABS_ALEXS_SECRET = "Venantonio (Clank) - Venantonio Labs: Alien Code: Alex's secret"
    VENANTONIO_LABS_HAROONS_SECRET = "Venantonio (Clank) - Venantonio Labs: Alien Code: Haroon's secret"
    GALACTIC_BOLT_RESERVE_AVERYS_SECRET = "Fort Sprocket (Clank) - Galactic Bolt Reserve: Alien Code: Avery's secret"
    GALACTIC_BOLT_RESERVE_LESLEYS_SECRET = "Fort Sprocket (Clank) - Galactic Bolt Reserve: Alien Code: Lesley's secret"
    GALACTIC_BOLT_RESERVE_DAVES_SECRET = "Fort Sprocket (Clank) - Galactic Bolt Reserve: Alien Code: Dave's secret"
    SPACESHIP_GRAVEYARD_MATTS_SECRET = "Spaceship Graveyard (Clank) - Spaceship Graveyard: Alien Code: Matt's secret"
    SPACESHIP_GRAVEYARD_KENS_SECRET = "Spaceship Graveyard (Clank) - Spaceship Graveyard: Alien Code: Ken's secret"
    SPACESHIP_GRAVEYARD_JAREDS_SECRET = "Spaceship Graveyard (Clank) - Spaceship Graveyard: Alien Code: Jared's secret"
    UNDERWATER_BUNKER_VESSUPS_SECRET = "Hydrano (Clank) - Underwater Bunker: Alien Code: Vessup's secret"
    UNDERWATER_BUNKER_ADAMS_SECRET = "Hydrano (Clank) - Underwater Bunker: Alien Code: Adam's secret"
    UNDERWATER_BUNKER_JEFFS_SECRET = "Hydrano (Clank) - Underwater Bunker: Alien Code: Jeff's secret"


# Native module ID (from GLOBALVARS_GetTotalAlienCodeCount, not a catalog ID)
# -> its Alien Codes, in flag-bit order.
ALIEN_CODES_BY_MODULE: dict[int, tuple[str, ...]] = {
    1: (
        SACAlienCodeLocations.BOLTAIRE_MUSEUM_THE_LEGENDS,
        SACAlienCodeLocations.BOLTAIRE_MUSEUM_RONNS_SECRET,
        SACAlienCodeLocations.BOLTAIRE_MUSEUM_BENS_SECRET,
    ),
    4: (
        SACAlienCodeLocations.ASYANICA_ROOFTOPS_JHAIROS_SECRET,
        SACAlienCodeLocations.ASYANICA_ROOFTOPS_GILBERTS_SECRET,
        SACAlienCodeLocations.ASYANICA_ROOFTOPS_RICARDOS_SECRET,
    ),
    10: (
        SACAlienCodeLocations.AZCOTAL_ALLEY_JONS_SECRET,
        SACAlienCodeLocations.AZCOTAL_ALLEY_THE_3_JASONS_SECRET,
        SACAlienCodeLocations.AZCOTAL_ALLEY_TRAVIS_SECRET,
    ),
    11: (
        SACAlienCodeLocations.GONDOLA_ASCENT_LEVITICUS_SECRET,
        SACAlienCodeLocations.GONDOLA_ASCENT_CARLS_SECRET,
        SACAlienCodeLocations.GONDOLA_ASCENT_JESS_SECRET,
    ),
    13: (
        SACAlienCodeLocations.HIGH_ROLLERS_CASINO_COLINS_SECRET,
        SACAlienCodeLocations.HIGH_ROLLERS_CASINO_SHANES_SECRET,
        SACAlienCodeLocations.HIGH_ROLLERS_CASINO_THE_PING_PONG_SECRET,
    ),
    16: (
        SACAlienCodeLocations.VENANTONIO_LABS_GERARDS_SECRET,
        SACAlienCodeLocations.VENANTONIO_LABS_ALEXS_SECRET,
        SACAlienCodeLocations.VENANTONIO_LABS_HAROONS_SECRET,
    ),
    19: (
        SACAlienCodeLocations.GALACTIC_BOLT_RESERVE_AVERYS_SECRET,
        SACAlienCodeLocations.GALACTIC_BOLT_RESERVE_LESLEYS_SECRET,
        SACAlienCodeLocations.GALACTIC_BOLT_RESERVE_DAVES_SECRET,
    ),
    22: (
        SACAlienCodeLocations.SPACESHIP_GRAVEYARD_MATTS_SECRET,
        SACAlienCodeLocations.SPACESHIP_GRAVEYARD_KENS_SECRET,
        SACAlienCodeLocations.SPACESHIP_GRAVEYARD_JAREDS_SECRET,
    ),
    29: (
        SACAlienCodeLocations.UNDERWATER_BUNKER_VESSUPS_SECRET,
        SACAlienCodeLocations.UNDERWATER_BUNKER_ADAMS_SECRET,
        SACAlienCodeLocations.UNDERWATER_BUNKER_JEFFS_SECRET,
    ),
}
