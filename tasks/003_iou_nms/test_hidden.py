import copy

import pytest

from solution import iou, nms


# ---------- iou ----------

def test_identical_boxes():
    assert iou((0, 0, 10, 10), (0, 0, 10, 10)) == pytest.approx(1.0)


def test_partial_overlap():
    # intersection 5x5=25, union 100+100-25=175
    assert iou((0, 0, 10, 10), (5, 5, 15, 15)) == pytest.approx(25 / 175)


def test_no_overlap():
    assert iou((0, 0, 10, 10), (20, 20, 30, 30)) == 0.0


def test_touching_edge_is_zero():
    assert iou((0, 0, 10, 10), (10, 0, 20, 10)) == 0.0


def test_box_inside_other():
    assert iou((0, 0, 10, 10), (2, 2, 7, 7)) == pytest.approx(25 / 100)


def test_zero_area_boxes_do_not_divide_by_zero():
    assert iou((5, 5, 5, 5), (5, 5, 5, 5)) == 0.0


def test_float_coordinates():
    assert iou((0.0, 0.0, 1.0, 1.0), (0.5, 0.0, 1.5, 1.0)) == pytest.approx(0.5 / 1.5)


def test_iou_is_symmetric():
    a, b = (0, 0, 10, 4), (3, 1, 12, 9)
    assert iou(a, b) == pytest.approx(iou(b, a))


# ---------- nms ----------

def test_example_from_prompt():
    boxes = [(0, 0, 10, 10), (1, 1, 11, 11), (50, 50, 60, 60)]
    assert nms(boxes, [0.9, 0.8, 0.7], 0.5) == [0, 2]


def test_empty():
    assert nms([], [], 0.5) == []


def test_order_follows_score_not_input_order():
    boxes = [(50, 50, 60, 60), (0, 0, 10, 10), (1, 1, 11, 11)]
    scores = [0.3, 0.6, 0.9]
    assert nms(boxes, scores, 0.5) == [2, 0]


def test_tie_breaks_by_lower_index():
    boxes = [(0, 0, 10, 10), (0, 0, 10, 10)]
    assert nms(boxes, [0.8, 0.8], 0.5) == [0]


def test_threshold_is_strictly_greater():
    # IoU of these two boxes is exactly 0.5 -> must be kept
    boxes = [(0, 0, 10, 10), (0, 0, 10, 20)]
    assert iou(*boxes) == pytest.approx(0.5)
    assert nms(boxes, [0.9, 0.8], 0.5) == [0, 1]


def test_suppression_is_against_kept_boxes_only():
    # B overlaps A (suppressed). C overlaps B but not A -> C must be kept.
    a = (0, 0, 10, 10)
    b = (4, 0, 14, 10)
    c = (9, 0, 19, 10)
    assert iou(a, b) > 0.3 and iou(b, c) > 0.3 and iou(a, c) < 0.3
    assert nms([a, b, c], [0.9, 0.8, 0.7], 0.3) == [0, 2]


def test_mismatched_lengths_raise():
    with pytest.raises(ValueError):
        nms([(0, 0, 1, 1)], [0.9, 0.8], 0.5)


def test_does_not_mutate_inputs():
    boxes = [(1, 1, 11, 11), (0, 0, 10, 10)]
    scores = [0.5, 0.9]
    b_copy, s_copy = copy.deepcopy(boxes), copy.deepcopy(scores)
    nms(boxes, scores, 0.5)
    assert boxes == b_copy and scores == s_copy
