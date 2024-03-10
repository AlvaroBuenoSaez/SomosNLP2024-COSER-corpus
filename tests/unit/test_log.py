import pytest

from module.common.configuration.config import get_logger
logger=get_logger("test")

def test_log():
    for level in ["trace","debug","info","success","warning","error","critical"]:
        getattr(logger,level)("{} message".format(level.upper()))