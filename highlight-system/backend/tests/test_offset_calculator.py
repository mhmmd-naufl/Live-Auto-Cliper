import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.offset_calculator import calculate_offset, calculate_cut_point, PRE_ROLL


def test_calculate_offset_normal():
    # buffer 60s, elapsed 10s -> offset 50
    assert calculate_offset(100.0, 110.0, 60.0) == 50.0


def test_calculate_offset_clamped_min():
    # elapsed longer than buffer -> offset 0
    assert calculate_offset(100.0, 200.0, 60.0) == 0.0


def test_calculate_offset_clamped_max():
    # negative elapsed -> offset buffer
    assert calculate_offset(100.0, 90.0, 60.0) == 60.0


def test_calculate_cut_point_includes_pre_roll():
    info = calculate_cut_point(100.0, 110.0, 60.0)
    assert info["offset"] == 50.0
    assert info["pre_roll"] == PRE_ROLL
    assert info["cut_start"] == round(max(0.0, 50.0 - PRE_ROLL), 2)


def test_calculate_cut_point_no_negative():
    info = calculate_cut_point(100.0, 100.0 + 59.0, 60.0)
    # offset 1, pre_roll 5 -> cut_start 0 (clamped)
    assert info["cut_start"] >= 0.0