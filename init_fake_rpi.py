import sys
import os

def _check_proc_files_for_rpi() -> bool:
    cpuinfo_path = '/proc/cpuinfo'
    if not os.path.exists(cpuinfo_path):
        return False

    try:
        with open(cpuinfo_path, 'r') as f:
            content = f.read()
        return 'Raspberry Pi' in content

    except Exception:
        return False

IS_REAL_RPI = _check_proc_files_for_rpi()

if not IS_REAL_RPI:
    # check if fake_rpi has been imported
    if 'fake_rpi' not in sys.modules:
        import fake_rpi
        sys.modules['RPi'] = fake_rpi.RPi  # Fake RPi
        sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO  # Fake GPIO
        sys.modules['smbus'] = fake_rpi.smbus  # Fake smbus (I2C)
