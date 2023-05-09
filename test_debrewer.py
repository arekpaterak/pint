import unittest
import os

DEBREWER_PATH = ".\\debrewer.py"
EXAMPLES_DIR = ".\\examples"


class TestDebrewer(unittest.TestCase):
    def test_examples(self):
        failed = False

        for filename in os.listdir(EXAMPLES_DIR):
            if filename.endswith(".pint") or filename.endswith(".🍺"):
                input_file = os.path.join(EXAMPLES_DIR, filename)
                input_pathname, input_extension = os.path.splitext(input_file)
                output_file = input_pathname + ".py"
                test_output_file = input_pathname + "_test.py"

                os.system(
                    f"python {DEBREWER_PATH} {input_file} -o {test_output_file}"
                )

                with open(output_file, "r", encoding="utf8") as f:
                    expected = f.read()
                with open(test_output_file, "r", encoding="utf8") as f:
                    actual = f.read()

                try:
                    self.assertEqual(expected, actual)
                except AssertionError:
                    print(f"File {filename} failed")
                    failed = True

                print(f"File {filename} OK")
                os.remove(test_output_file)

        if failed:
            self.fail("Some tests failed")
