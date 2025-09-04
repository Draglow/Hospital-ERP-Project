# Apps package
# This package provides compatibility for imports that expect apps.* structure

# Import the actual apps to make them available under the apps namespace
import sys
import os

# Add the parent directory to the path so we can import the actual apps
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import the actual apps
try:
    import appointments
    import notifications
    import patients
    import doctors
    import billing
    import pharmacy
    import accounts
except ImportError:
    # If direct imports fail, that's okay
    pass
