import os
import tempfile
import unittest

from Skill.file_io import read_file


class FileIOTests(unittest.TestCase):
    def test_read_text_file_returns_content(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as handle:
            handle.write("hello from a text file")
            temp_path = handle.name

        try:
            result = read_file(temp_path)
            self.assertEqual(result["content"], "hello from a text file")
        finally:
            os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()
