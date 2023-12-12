# txtar

`txtar` is a Python reimplementation of Go's txtar format, a tool for bundling and managing multiple text files in a single archive.

## Features

- Parse `txtar` formatted text into structured data.
- Serialize structured data back into `txtar` format.
- Unpack `txtar` archives into the file system.


## Usage

### In unit tests

```python
from pathlib import Path
import os

def test_my_function():
    # Define the txtar structure for sysfs-like files
    txtar_content = """
-- sys/class/thermal/thermal_zone0/temp --
55000
-- sys/class/power_supply/BAT0/capacity --
45
-- sys/block/sda/size --
1024000
"""

    with MockFS.from_string(txtar_content):
        assert os.path.exists("/sys/class/thermal/thermal_zone0/temp")
        assert os.path.exists("/sys/class/power_supply/BAT0/capacity")
        assert os.path.exists("/sys/block/sda/size")

        assert Path("/sys/block/sda/size").exists()
```

### Reading a file
```python
from txtar import TxTar

content = "..."  # txtar formatted string
archive = TxTar.parse(content)
```

### Serializing to txtar Format

```python
from txtar import TxTar, File

archive = TxTar(
    comments=["Example txtar archive"],
    files=[File(name="example.txt", lines=["Hello", "World"])]
)
content = archive.serialize()
```

### Unpacking an Archive

```python
from pathlib import Path
from txtar import TxTar

archive = TxTar.parse("...")
archive.unpack_in(Path("/path/to/unpack"))
```

## Development

 * Install dependencies: `poetry install`
 * Run tests with `pytest`.

## Releasing

```
poetry publish --build --username __token__ --password $PYPI_PASSWORD
```
