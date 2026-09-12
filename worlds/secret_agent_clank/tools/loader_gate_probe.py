"""Hold one native reset after relocation, inspect exports, then release.

No inventory or location changes. Restores the resident instruction on normal
completion, timeout, or Python exception. Do not kill the process while armed.
"""
import importlib.util
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pypine import Pine


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    Gate = load('loader_gate', 'core/loader_gate.py').LoaderGate
    Symbols = load('symbols', 'core/symbols.py').RuntimeSymbols
    p = Pine(28011)
    p.connect()
    gate = Gate(p)
    journal = ROOT / '.research/loader_gate_probe.json'
    record = {'site': gate.SITE, 'original': gate.ORIGINAL, 'replacement': gate.HELD,
              'armed': False, 'held': False}
    try:
        gate.validate()
        record['armed'] = True
        journal.write_text(json.dumps(record, indent=2))
        gate.arm()
        print('ARMED: use the in-game level reset now.', flush=True)
        deadline = time.monotonic() + 180
        while time.monotonic() < deadline:
            target = gate.held_module()
            if target is not None:
                record['held'] = True
                record['target'] = target
                symbols = Symbols(p)
                symbols.refresh()
                record['exports'] = {name: symbols.get(name) for name in (
                    'WeaponPickup_GiveWeapon__FP4Moby', 'LEVEL_LoadLevel__FPCc',
                    'MOBY_InitMobys__Fv', 'main_GameStart__Fi')}
                record['stable_after_read'] = gate.held_module() == target
                print(json.dumps(record), flush=True)
                break
            time.sleep(0.1)
        else:
            record['timed_out'] = True
    finally:
        try:
            gate.release()
            record['armed'] = False
            record['restored'] = True
            print('Resident loader instruction restored.', flush=True)
        finally:
            journal.write_text(json.dumps(record, indent=2))
            p.disconnect()


if __name__ == '__main__':
    main()
