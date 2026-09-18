"""SAC-style receipt colours for the non-blocking item HUD."""


def receipt_text(item, sender, trap=False):
    def clean(value, limit):
        value = ''.join(c if 32 <= ord(c) < 127 else '?' for c in str(value))
        return value if len(value) <= limit else value[:limit - 3] + '...'
    colour = 3 if trap else 13
    return (b'Received ' + bytes((0x90, colour)) + clean(item, 32).encode('ascii')
            + b'\x90\x01\nfrom \x90\x0b' + clean(sender, 30).encode('ascii')
            + b'\x90\x01\0')
