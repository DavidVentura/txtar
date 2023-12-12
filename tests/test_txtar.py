from txtar import TxTar, File

# Example cases come from
# https://cs.opensource.google/go/x/tools/+/refs/tags/v0.16.0:txtar/archive_test.go;l=21
example_text_payload = """comment1
comment2
-- file1 --
File 1 text.
-- foo ---
More file 1 text.
-- file 2 --
File 2 text.
-- empty --
-- noNL --
hello world
-- empty filename line --
some content
-- --"""

example_structured_payload = TxTar(
    comments=["comment1", "comment2"],
    files=[
        File(name="file1", lines=["File 1 text.", "-- foo ---", "More file 1 text."]),
        File(name="file 2", lines=["File 2 text."]),
        File(name="empty", lines=[]),
        File(name="noNL", lines=["hello world"]),
        File(name="empty filename line", lines=["some content", "-- --"]),
    ],
)


def test_txtar_archive_parse():
    assert TxTar.parse(example_text_payload) == example_structured_payload


def test_txtar_archive_serialize():
    assert example_text_payload == example_structured_payload.serialize()


def test_extraction(tmp_path):
    example_structured_payload.unpack_in(tmp_path)
    found_files = list(tmp_path.glob("**/*"))
    assert sorted(found_files) == sorted(["file1", "file 2", "empty", "noNL", "empty filename line"])


def test_extraction_with_subdir(tmp_path):
    parsed = TxTar.parse(
        """
-- a/file/in/a/dir/filename --
content
"""
    )
    parsed.unpack_in(tmp_path)

    expected_path = tmp_path / "a/file/in/a/dir/filename"
    assert expected_path.exists()
    assert expected_path.read_text() == "content"
