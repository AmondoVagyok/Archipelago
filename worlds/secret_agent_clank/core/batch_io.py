_SIZES = (8, 4, 2, 1)


def _chunks(address, length):
    """The (size, address) pieces PINE's own read_bytes/write_bytes would use for one block."""
    chunks = []
    offset = 0
    while offset < length:
        size = next(size for size in _SIZES if size <= length - offset)
        chunks.append((size, address + offset))
        offset += size
    return chunks


def read_blocks(pine, spans):
    pieces = [_chunks(address, length) for address, length in spans]
    values = iter(pine.batch_read([chunk for chunks in pieces for chunk in chunks]))
    return [b"".join(next(values).to_bytes(size, "little") for size, _ in chunks) for chunks in pieces]


def write_blocks(pine, blocks):
    """Write every (address, data) block in one request, in order."""
    pine.batch_write([
        (size, chunk, data[chunk - address:chunk - address + size])
        for address, data in blocks
        for size, chunk in _chunks(address, len(data))
    ])
