# Task 003 - IoU and Non-Maximum Suppression

Object detectors output many overlapping boxes for the same object. Write two Python functions.

Boxes are tuples `(x1, y1, x2, y2)` in pixels, with `x1 <= x2` and `y1 <= y2`.

## 1. `iou(box_a, box_b) -> float`

Return the Intersection over Union of two boxes:

```
iou = intersection_area / (area_a + area_b - intersection_area)
```

- Boxes that do not overlap, or only touch at an edge, return `0.0`.
- If the union area is `0` (both boxes have zero area), return `0.0`.

## 2. `nms(boxes, scores, iou_threshold) -> list[int]`

Greedy Non-Maximum Suppression:

1. Sort boxes by score, highest first. If two scores are equal, the box with the lower original index comes first.
2. Keep the first box. Remove every remaining box whose IoU with it is **greater than** `iou_threshold`.
3. Repeat with the next remaining box.

Return the **original indices** of the kept boxes, in the order they were kept (highest score first).

- `boxes` and `scores` must have the same length; otherwise raise `ValueError`.
- Empty input returns `[]`.
- Do not modify the input lists.

Example:

```python
boxes = [(0, 0, 10, 10), (1, 1, 11, 11), (50, 50, 60, 60)]
scores = [0.9, 0.8, 0.7]
nms(boxes, scores, iou_threshold=0.5)
# [0, 2]
```

Write both functions in a single file `solution.py`.
