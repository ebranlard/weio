# Streaming Mode - Quick Reference

## For Users

### Header-only inspection (memory efficient!)
```python
import weio

with weio.read('large_file.outb', streaming=True) as f:
    print(f['attribute_names'])  # Column names
    print(f['attribute_units'])  # Units
    # f.data is None - no data loaded
```

### Load data after inspection
```python
import weio

with weio.read('file.out', streaming=True) as f:
    print(f"Channels: {len(f['attribute_names'])}")
    f.readAll()  # Load data now
    df = f.toDataFrame()
```

### Process CSV in chunks
```python
import weio

with weio.read('huge.csv', streaming=True) as f:
    while True:
        chunk = f.readChunk(nlines=10000)
        if chunk is None:
            break
        # Process chunk...
```

## For Developers

### Adding streaming to a new file format

1. **Add `streaming` parameter to `_read()`:**
```python
def _read(self, streaming=False, **kwargs):
    if streaming:
        # Read headers only, keep file open
        self._fid = open(self.filename, 'r')
        self['header'] = self._fid.readline()
        self.data = None
    else:
        # Normal mode: read everything
        with open(self.filename, 'r') as f:
            self.data = f.read()
```

2. **Implement `_readAll()`:**
```python
def _readAll(self):
    if self._fid is None:
        raise RuntimeError("No open file handle")
    # Read remaining data
    self.data = self._fid.read()
```

3. **Optional: Implement `_readChunk()`:**
```python
def _readChunk(self, nlines=None, **kwargs):
    if self._fid is None:
        raise RuntimeError("No open file handle")
    if nlines is None:
        nlines = 1000
    # Read chunk...
    return chunk  # or None if EOF
```

That's it! The base File class handles context managers and enforcement.

## Supported Formats (so far)

- ✅ **OpenFAST:** `.out` (ASCII), `.outb` (binary)
- ✅ **CSV:** `.csv`, `.txt` (with chunk reading)
- ✅ **HAWC2:** `.dat`, `.sel` (ASCII and binary)

## Key Design Points

- **Single `streaming` parameter** (not both `headerOnly` and `streaming`)
- **Context manager required** for streaming mode (`with` statement)
- **Header-only:** Exit `with` block without calling `readAll()`
- **Full streaming:** Call `readAll()` or `readChunk()` inside `with` block
- **Backward compatible:** Default `streaming=False` means existing code works unchanged
