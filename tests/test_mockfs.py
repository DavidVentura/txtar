import os
from pathlib import Path

from txtar import MockFS


def test_mockfs():
    txtar_content = """
-- sys/class/thermal/thermal_zone99/temp --
55000
-- sys/class/power_supply/BAT0/capacity --
45
-- sys/block/sda/size --
1024000
"""
    assert not os.path.exists("/sys/class/thermal/thermal_zone99/temp")
    assert not os.path.exists("/sys/class/power_supply/BAT0/capacity")
    assert not os.path.exists("/sys/block/sda/size")

    assert not Path("/sys/class/thermal/thermal_zone99/temp").exists()
    assert not Path("/sys/class/power_supply/BAT0/capacity").exists()
    assert not Path("/sys/block/sda/size").exists()

    with MockFS.from_string(txtar_content):
        assert os.path.exists("/sys/class/thermal/thermal_zone99/temp")
        assert os.path.exists("/sys/class/power_supply/BAT0/capacity")
        assert os.path.exists("/sys/block/sda/size")

        assert Path("/sys/class/thermal/thermal_zone99/temp").exists()
        assert Path("/sys/class/power_supply/BAT0/capacity").exists()
        assert Path("/sys/block/sda/size").exists()

        assert Path("/sys/class/thermal/thermal_zone99/temp").read_text() == "55000"
        assert Path("/sys/class/power_supply/BAT0/capacity").read_text() == "45"
        assert Path("/sys/block/sda/size").read_text() == "1024000"
