"""Only native multi-level weapons participate; tools stay single unlocks."""
from .weapons import RATCHET_WEAPON_DISPLAY_TO_INTERNAL, GADGET_DISPLAY_TO_INTERNAL
LEVELLED_INTERNALS = ('blaster', 'shardgun', 'beemineglove', 'shockrocket',
    'walloper', 'plasmawhip', 'porkbomb', 'minelauncher', 'ryno', 'throwTie',
    'CuffLink', 'TangleVine', 'HoloKnuckles', 'FlamethrowerPen', 'LightningUmbrella')
PROGRESSIVE_TO_INTERNAL = {
    name.replace('Unlock:', 'Progressive:', 1): internal
    for name, internal in {**RATCHET_WEAPON_DISPLAY_TO_INTERNAL, **GADGET_DISPLAY_TO_INTERNAL}.items()
    if internal in LEVELLED_INTERNALS
}
UNLOCK_TO_PROGRESSIVE = {
    name: name.replace('Unlock:', 'Progressive:', 1)
    for name, internal in {**RATCHET_WEAPON_DISPLAY_TO_INTERNAL, **GADGET_DISPLAY_TO_INTERNAL}.items()
    if internal in LEVELLED_INTERNALS
}
def max_level(internal, ng_plus):
    return 4 if internal == 'ryno' or not ng_plus else 8

TITAN_LOCATIONS = {internal: f'Titan Vendor: {internal}'
                   for internal in LEVELLED_INTERNALS if internal != 'ryno'}
TITAN_ITEMS = {f'Titan Upgrade: {internal}': internal for internal in TITAN_LOCATIONS}
