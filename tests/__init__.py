"""Test suite for RSA encryption package.

Ensure the local `src` package path is discoverable when running tests
without installing the package in editable mode. This mirrors `pip install -e .`
behavior for CI and local development.
"""

import os
import sys

# Insert the repository's src directory at the front of sys.path for test discovery
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)
