"""Read-only PINE capture/symbol inspection; run from any directory.

python tools/memory_probe.py status
python tools/memory_probe.py capture .research/before.bin
python tools/memory_probe.py symbols .research/before.bin --match WeaponPickup
python tools/memory_probe.py diff .research/before.bin .research/after.bin --start 0x206000 --size 0x2000
"""
import argparse
import importlib.util
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pypine import Pine

spec = importlib.util.spec_from_file_location("sac_symbols", ROOT / "core/symbols.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
RuntimeSymbols = module.RuntimeSymbols


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=28011)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    capture = sub.add_parser("capture")
    capture.add_argument("output", type=Path)
    symbols = sub.add_parser("symbols")
    symbols.add_argument("capture", type=Path)
    symbols.add_argument("--match", default="")
    diff = sub.add_parser("diff")
    diff.add_argument("before", type=Path)
    diff.add_argument("after", type=Path)
    diff.add_argument("--start", type=lambda v: int(v, 0), default=0)
    diff.add_argument("--size", type=lambda v: int(v, 0), default=0x2000000)
    args = parser.parse_args()
    if args.command == "symbols":
        data = args.capture.read_bytes()
        values = RuntimeSymbols.parse(data[0x600000:0x1000000], 0x600000)
        for name, value in sorted(values.items()):
            if args.match.lower() in name.lower():
                print(f"0x{value:08X} {name}")
        return
    if args.command == "diff":
        before, after = args.before.read_bytes(), args.after.read_bytes()
        for address in range(max(0, args.start), min(len(before), len(after), args.start + args.size)):
            if before[address] != after[address]:
                print(f"0x{address:08X}: {before[address]:02X} -> {after[address]:02X}")
        return
    pine = Pine(args.port)
    try:
        pine.connect()
        game = pine.get_game_id()
        if game != "SCUS-97623":
            raise RuntimeError(f"Expected SCUS-97623, found {game!r}")
        case = pine.read_int32(0x206328)
        status = {"game": game, "case": case, "requested_case": pine.read_int32(0x206324),
                  "bolts": pine.read_int32(0x2075C8), "emulator_status": int(pine.get_emu_status())}
        if args.command == "capture":
            output = args.output.resolve()
            if not output.is_relative_to(ROOT):
                raise ValueError("Capture output must stay inside secret_agent_clank")
            if output.exists():
                raise FileExistsError(output)
            data = b"".join(pine.read_bytes(a, 0x20000) for a in range(0, 0x2000000, 0x20000))
            if pine.read_int32(0x206328) != case:
                raise RuntimeError("Case changed during capture; retry from a stable level")
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(data)
            status["capture"] = str(output)
            status["atomic"] = False  # PINE reads are chunked; the emulator keeps running.
        print(json.dumps(status, indent=2))
    finally:
        pine.disconnect()


if __name__ == "__main__":
    main()
