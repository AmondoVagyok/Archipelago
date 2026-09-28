# Native vendor icon

`archipelago-icon.indices` and `archipelago-icon.clut` are the verified native
32×32 indexed texture and PS2 palette. The client loads these packaged assets
when displaying scouted AP vendor purchases. The TIM2 file is not used at runtime.

`core/vendor_rewards.py` manages row icons and selected reward text. It preserves
native prices, offer types, weapon IDs and mod IDs. Closing the vendor restores
the borrowed Shock Rocket texture. All AP purchase rows use the AP icon; unscouted rows keep equipment text until scouting completes. The AP catalog excludes ammo and non-location offers.

Text hooks install at the native loader gate, using verified unused debug drawing
code, independently of gain multiplier storage. Text shares the inactive native
HUD notification buffer; an active native hint defers the reward text until its
timer finishes. After updating the client, reset or change levels once to install
the hooks. Progression items use orange titles; other items use white titles.

The combined patch plans and runtime presentation are tested against local RAM
captures. The automatic path still needs visual verification in a running game.
