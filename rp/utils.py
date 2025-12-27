import os
import logging
import sys
from gpio_interface import GPIOInterface


_LOGGING_CONFIGURED = False
_DEBUG_CLASSES = {"RaspBerryPI"}

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

def get_gpio() -> GPIOInterface:
    if _check_proc_files_for_rpi():
        from real_gpio import RealGPIO
        return RealGPIO()
    else:
        from fake_gpio import FakeGPIO
        return FakeGPIO()

def configure_logging():
    global _LOGGING_CONFIGURED
    if _LOGGING_CONFIGURED:
        return

    global_level = logging.INFO
    root = logging.getLogger()
    root.handlers.clear()
    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    root.setLevel(global_level)

    for cls_name in _DEBUG_CLASSES:
        logger = logging.getLogger(cls_name)
        logger.setLevel(logging.DEBUG)

    _LOGGING_CONFIGURED = True

def get_logger(cls) -> logging.Logger:
    configure_logging()
    logger = logging.getLogger(cls.__name__)
    return logger


try:
    import msvcrt
    def key_pressed():
        return msvcrt.kbhit()
    def consume_key():
        msvcrt.getch()
except ImportError:
    import select
    def key_pressed():
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        return bool(dr)
    def consume_key():
        try:
            sys.stdin.read(1)
        except Exception:
            pass