import copy

import pytest

from solution import dwell_times


def test_example_from_prompt():
    dets = [(0, 7, "person"), (29, 7, "person"), (10, 8, "car")]
    assert dwell_times(dets, fps=30) == {7: 1.0, 8: 0.03}


def test_empty():
    assert dwell_times([], fps=30) == {}


def test_single_frame_counts_as_one_frame():
    assert dwell_times([(100, 1, "person")], fps=10) == {1: 0.1}


def test_unordered_input():
    dets = [(50, 1, "person"), (0, 1, "person"), (25, 1, "person")]
    assert dwell_times(dets, fps=25) == {1: 2.04}


def test_gaps_are_counted():
    dets = [(0, 3, "car"), (299, 3, "car")]  # no detections in between
    assert dwell_times(dets, fps=30) == {3: 10.0}


def test_duplicates_do_not_change_result():
    dets = [(0, 1, "p"), (0, 1, "p"), (9, 1, "p"), (9, 1, "p")]
    assert dwell_times(dets, fps=10) == {1: 1.0}


def test_label_is_ignored():
    dets = [(0, 1, "person"), (9, 1, "unknown")]
    assert dwell_times(dets, fps=10) == {1: 1.0}


def test_float_fps():
    dets = [(0, 1, "p"), (29, 1, "p")]
    assert dwell_times(dets, fps=29.97) == {1: 1.0}


def test_many_tracks():
    dets = [(f, tid, "p") for tid in range(1000) for f in (tid, tid + 59)]
    result = dwell_times(dets, fps=60)
    assert len(result) == 1000
    assert all(v == 1.0 for v in result.values())


@pytest.mark.parametrize("bad_fps", [0, -30, None, "30"])
def test_invalid_fps_raises(bad_fps):
    with pytest.raises(ValueError):
        dwell_times([(0, 1, "p")], fps=bad_fps)


def test_does_not_mutate_input():
    dets = [(9, 1, "p"), (0, 1, "p")]
    snapshot = copy.deepcopy(dets)
    dwell_times(dets, fps=10)
    assert dets == snapshot
