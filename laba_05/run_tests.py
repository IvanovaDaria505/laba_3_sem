import unittest
import sys
from pathlib import Path

LAB5_DIR = Path(__file__).resolve().parent
PROJECT_DIR = LAB5_DIR.parent

sys.path.insert(0, str(PROJECT_DIR / "laba_04"))
sys.path.insert(0, str(PROJECT_DIR / "laba_03"))

def run_tests():
    loader = unittest.TestLoader()

    suite = loader.discover(
        start_dir=str(LAB5_DIR),
        pattern="test_*.py"
    )

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()

if __name__ == "__main__":
    sys.exit(0 if run_tests() else 1)
