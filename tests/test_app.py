# tests/test_app.py
import io
import runpy
import unittest
from contextlib import redirect_stdout

from app import greet


class TestApp(unittest.TestCase):

    def test_greet(self):
        self.assertEqual(greet("World"), "Hello, World from Karim Zarzour!")

    def test_greet_other_name(self):
        self.assertEqual(greet("Jenkins"),
                         "Hello, Jenkins from Karim Zarzour!")

    def test_main_prints_greeting(self):
        output = io.StringIO()
        with redirect_stdout(output):
            runpy.run_module("app", run_name="__main__")
        self.assertEqual(output.getvalue().strip(),
                         "Hello, World from Karim Zarzour!")


if __name__ == "__main__":
    unittest.main()
