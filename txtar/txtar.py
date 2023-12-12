from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from pyfakefs.fake_filesystem_unittest import Patcher


@dataclass
class File:
    name: str
    lines: list[str]


@dataclass
class TxTar:
    comments: list[str]
    files: list[File]

    @staticmethod
    def parse(content: str) -> "TxTar":
        filename = None
        files = []
        file_content = []
        comments = []

        for line in content.splitlines():
            if line.startswith("-- ") and line.endswith(" --") and len(line) > 5:
                new_filename = line[3:-3]
                if len(new_filename) > 0:
                    # Specifically disallow "-- --" as a valid separator
                    if filename is not None:
                        files.append(File(name=filename, lines=file_content))
                    file_content = []
                    filename = new_filename
                    continue

            if filename is None:
                comments.append(line)
                continue

            file_content.append(line)

        if filename is not None:
            files.append(File(name=filename, lines=file_content))

        return TxTar(comments=comments, files=files)

    def serialize(self) -> str:
        ret = []
        ret.extend(self.comments)
        for f in self.files:
            ret.append(f"-- {f.name} --")
            ret.extend(f.lines)

        return "\n".join(ret)

    def unpack_in(self, dest: Path):
        if not dest.exists():
            dest.mkdir()

        for f in self.files:
            fpath = dest / f.name
            fdir = fpath.parent
            if fdir != dest and not fdir.exists():
                fdir.mkdir(parents=True)

            with fpath.open("w") as fd:
                fd.write("\n".join(f.lines))


class MockFS:
    def __init__(self, txtar: TxTar):
        self.txtar = txtar
        self.patcher = None

    @staticmethod
    def from_string(content: str):
        return MockFS(txtar=TxTar.parse(content))

    def __enter__(self):
        self.patcher = Patcher().__enter__()
        for file in self.txtar.files:
            self.patcher.fs.create_file(file.name, contents="\n".join(file.lines))
        return self

    def __exit__(self, *exc) -> Optional[bool]:
        if self.patcher:
            return self.patcher.__exit__(*exc)
