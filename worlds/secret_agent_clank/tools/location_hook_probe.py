"""Read or restore a previously journaled native location-hook test.

python -B tools/location_hook_probe.py status .research/vendor_hook_test_v2.json
python -B tools/location_hook_probe.py restore .research/vendor_hook_test_v2.json

Restoration requires the original module and an open vendor/Case Files screen.
It restores code only; separately recorded funding or inventory test changes
must be reconciled explicitly rather than guessing whether a purchase occurred.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pypine import Pine

spec = importlib.util.spec_from_file_location('sac_location_hooks', ROOT / 'core/location_hooks.py')
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('status', 'restore'))
    parser.add_argument('journal', type=Path)
    args = parser.parse_args()
    journal = args.journal.resolve()
    if not journal.is_relative_to(ROOT):
        raise ValueError('Journal must remain inside Secret Agent Clank')
    record = json.loads(journal.read_text())
    pine = Pine(28011)
    pine.connect()
    try:
        if pine.get_game_id() != 'SCUS-97623':
            raise RuntimeError('Wrong game')
        current = pine.read_int32(0x206328)
        if current != record['module']:
            raise RuntimeError(f'Module changed to {current}; old addresses must not be used')
        hooks = module.LocationHooks(pine)
        hooks.module = record['module']
        hooks.marker_address = record['marker_address']
        hooks.tables = record['tables']
        hooks.locations = {kind: {int(k): v for k, v in values.items()}
                           for kind, values in record['locations'].items()}
        hooks.patches = [module.Patch(x['address'], bytes.fromhex(x['original']),
                                     bytes.fromhex(x['replacement'])) for x in record['patches']]
        hooks.installed = record.get('installed', False)
        if args.command == 'restore':
            if pine.read_int32(record['screen_address']) not in (8, 14, 16):
                raise RuntimeError('Open vendor or Case Files before restoring code')
            hooks.restore()
            for patch in hooks.patches:
                if pine.read_bytes(patch.address, len(patch.original)) != patch.original:
                    raise RuntimeError('Restoration readback failed')
            record['installed'] = False
            record['restored'] = True
            journal.write_text(json.dumps(record, indent=2))
        else:
            print(json.dumps({'module': current, 'screen': pine.read_int32(record['screen_address']),
                              'bolts': pine.read_int32(0x2075C8),
                              'location_flags': {kind: {name: pine.read_int8(hooks.tables[kind] + slot)
                                                       for slot, name in values.items()}
                                                 for kind, values in hooks.locations.items()},
                              'native_events': hooks.poll()}, indent=2))
    finally:
        pine.disconnect()


if __name__ == '__main__':
    main()
