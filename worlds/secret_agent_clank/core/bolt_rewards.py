"""Deliver AP currency once per received item, with a per-slot local journal."""
import hashlib
import json
from pathlib import Path
from .address_maps import BOLTS_ADDRESS

def reward_balance(balance, count):
    for _ in range(count):
        updated = min(0x7FFFFFFF, balance + balance // 5)
        if updated == balance:
            break
        balance = updated
    return balance


class BoltRewards:
    def __init__(self, pine, log):
        self.pine = pine
        self.log = log
        self.path = None
        self.received = 0
        self.starting_bolts = 0
        self.state = {'delivered': 0, 'pending': None}

    def configure(self, seed, team, slot, directory=None, *, starting_bolts=0):
        if type(starting_bolts) is not int or not 0 <= starting_bolts <= 100_000:
            raise ValueError('Starting bolts must be between 0 and 100000')
        self.starting_bolts = starting_bolts
        if seed is None or team is None or slot is None:
            return
        directory = Path(directory) if directory is not None else Path(__file__).resolve().parents[1] / '.client_state'
        key = hashlib.sha256(json.dumps([seed, team, slot]).encode()).hexdigest()
        path = directory / (key + '.json')
        if path == self.path:
            return
        state = json.loads(path.read_text()) if path.exists() else {'delivered': 0, 'pending': None}
        if type(state.get('delivered')) is not int or state['delivered'] < 0:
            raise ValueError('Invalid bolt reward journal')
        self.path, self.state, self.received = path, state, 0

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix('.tmp')
        temporary.write_text(json.dumps(self.state))
        temporary.replace(self.path)

    def deliver(self):
        # Called only after the native runtime and current level are ready.
        if self.path is None:
            return
        pending = self.state.get('pending')
        if pending:
            current = self.pine.read_int32(BOLTS_ADDRESS)
            if current == pending['before']:
                self.pine.write_int32(BOLTS_ADDRESS, pending['after'])
            elif current != pending['after']:
                raise RuntimeError('An interrupted bolt reward has an uncertain balance; '
                                   'delivery is paused to avoid duplicating or overwriting bolts.')
            if pending.get('kind') == 'starting':
                self.state['starting_delivered'] = True
            else:
                self.state['delivered'] = pending['count']
            self.state['pending'] = None
            self._save()
        if not self.state.get('starting_delivered', False):
            before = self.pine.read_int32(BOLTS_ADDRESS)
            after = min(0x7FFFFFFF, before + self.starting_bolts)
            # Award once, preserving bolts already earned while connecting.
            # Use the same write-ahead recovery as received percentage items.
            self.state['pending'] = {'kind': 'starting', 'before': before, 'after': after}
            self._save()
            if after != before:
                self.pine.write_int32(BOLTS_ADDRESS, after)
            self.state.update(starting_delivered=True, pending=None)
            self._save()
            if self.starting_bolts:
                self.log(f'[SAC] Granted {after - before:,} starting bolts.')
        count = self.received - self.state['delivered']
        if count <= 0:
            return
        before = self.pine.read_int32(BOLTS_ADDRESS)
        after = reward_balance(before, count)
        self.state['pending'] = {'before': before, 'after': after, 'count': self.received}
        self._save()
        self.pine.write_int32(BOLTS_ADDRESS, after)
        self.state.update(delivered=self.received, pending=None)
        self._save()
        self.log(f'[SAC] Received {after - before:,} bolts from {count} AP bolt item(s).')
