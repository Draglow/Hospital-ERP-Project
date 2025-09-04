# Apps appointments package
# This provides compatibility for imports that expect apps.appointments structure

# Import from the actual appointments app
import sys
import os

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the actual appointments module
try:
    from appointments import *
except ImportError:
    pass
