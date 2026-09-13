"""One Boltaire reset: install an unchecked Tie pickup with pre-init ownership.

Leaves journaled location hooks installed for visual inspection. Always releases
the resident loader barrier before disconnecting. Restore location hooks with
location_hook_probe.py while Case Files is open after the test.
"""
import importlib.util
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pypine import Pine


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'core' / (name + '.py'))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def load_package(name):
    """Like load(), but for a core/<name>/ package (relative imports inside
    it need __path__ set, which a bare file load doesn't give them)."""
    package_dir = ROOT / 'core' / name
    spec = importlib.util.spec_from_file_location(
        name, package_dir / '__init__.py', submodule_search_locations=[str(package_dir)],
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def main():
    Gate = load('loader_gate').LoaderGate
    Symbols = load('symbols').RuntimeSymbols
    Hooks = load_package('patches').LocationHooks
    p = Pine(28011)
    p.connect()
    gate = Gate(p)
    path = ROOT / '.research/early_tie_pickup_test.json'
    record = {'installed': False, 'loader_armed': False}

    def save():
        path.write_text(json.dumps(record, indent=2))

    try:
        gate.validate()
        if p.read_int32(0x206328) != 1 or p.read_int32(0x206324) != 0xFFFFFFFF:
            raise RuntimeError('Start from settled Boltaire Museum')
        record['loader_site'] = gate.SITE
        record['loader_original'] = gate.ORIGINAL
        record['loader_armed'] = True
        save()
        gate.arm()
        print('ARMED: reset Boltaire in-game, then leave the Tie pickup uncollected.', flush=True)
        deadline = time.monotonic() + 180
        while time.monotonic() < deadline:
            target = gate.held_module()
            if target is not None:
                if target != 1:
                    raise RuntimeError('This experiment supports only Boltaire Museum')
                symbols = Symbols(p)
                symbols.refresh()
                hooks = Hooks(p)
                hooks.prepare(symbols, pickup_locations={11: 'throwTie'}, vendor_locations={},
                              entitlements={11: True})
                base = symbols.get('GADGET_g_GadgetList')
                if base is None or not 0x100000 <= base < 0x2000000 - 40 * 0x74:
                    raise RuntimeError('Invalid gadget table')
                record.update(module=target, marker_address=hooks.marker_address,
                              tables=hooks.tables, locations=hooks.locations,
                              entitlement_table=hooks.entitlement_table,
                              screen_address=6629900, owned_address=base + 11 * 0x74 + 0x70,
                              patches=[{'address': x.address, 'original': x.original.hex(),
                                        'replacement': x.replacement.hex()} for x in hooks.patches])
                save()  # Recovery data precedes any module code writes.
                hooks.install_at_loader_gate(gate)
                record['installed'] = True
                save()
                gate.release()
                record['loader_armed'] = False
                save()
                deadline_init = time.monotonic() + 45
                while time.monotonic() < deadline_init:
                    if not hooks.is_current():
                        raise RuntimeError('Module or marker changed during startup')
                    count = p.read_int8(hooks.entitlement_table + 40)
                    if count:
                        record['startup_result'] = {
                            'init_invocations': count,
                            'owned': p.read_int32(record['owned_address']),
                            'pickup_flag': p.read_int8(hooks.tables['pickup'] + 11),
                        }
                        save()
                        print(json.dumps(record['startup_result']), flush=True)
                        print('Hooks remain installed. Inspect the Tie pickup and pause before collecting.', flush=True)
                        return
                    time.sleep(0.1)
                raise RuntimeError('Object initialization was not observed within 45 seconds')
            time.sleep(0.1)
        record['timed_out'] = True
    except Exception as exc:
        record['error'] = str(exc)
        raise
    finally:
        try:
            gate.release()
            record['loader_armed'] = False
            record['loader_restored'] = True
        finally:
            save()
            p.disconnect()


if __name__ == '__main__':
    main()
