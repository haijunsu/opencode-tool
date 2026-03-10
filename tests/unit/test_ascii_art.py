import unittest
from io import StringIO
from unittest.mock import patch
from opencode_tool.ascii_art import ascii_art, main


class TestAsciiArt(unittest.TestCase):
    def test_ascii_art_basic(self):
        output = ascii_art("hi")
        self.assertIn("#", output)
        self.assertEqual(len(output.split("\n")), 7)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("sys.argv", ["ascii_art.py", "test"])
    def test_main_with_args(self, mock_stdout):
        main()
        output = mock_stdout.getvalue()
        self.assertIn("#", output)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("sys.stdin.isatty", return_value=False)
    @patch("sys.stdin.read", return_value="piped")
    @patch("sys.argv", ["ascii_art.py"])
    def test_main_with_piped_input(self, mock_read, mock_isatty, mock_stdout):
        main()
        output = mock_stdout.getvalue()
        self.assertIn("#", output)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("sys.stdin.isatty", return_value=True)
    @patch("builtins.input", side_effect=EOFError)
    @patch("sys.argv", ["ascii_art.py"])
    def test_main_with_eof_error(self, mock_input, mock_isatty, mock_stdout):
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
