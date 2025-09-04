# Apps appointments signals
# This provides compatibility for imports that expect apps.appointments.signals

# Import from the actual appointments signals
import sys
import os

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the actual signals from appointments.signals
try:
    from appointments.signals import *
except ImportError:
    # If appointments.signals doesn't exist, import from notifications.signals
    try:
        from notifications.signals import (
            appointment_notifications,
            appointment_status_change_notifications
        )
    except ImportError:
        pass
