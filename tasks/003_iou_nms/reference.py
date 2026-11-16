def _area(box):
    x1, y1, x2, y2 = box
    return max(0.0, x2 - x1) * max(0.0, y2 - y1)


def iou(box_a, box_b) -> float:
    ix1 = max(box_a[0], box_b[0])
    iy1 = max(box_a[1], box_b[1])
    ix2 = min(box_a[2], box_b[2])
    iy2 = min(box_a[3], box_b[3])
    inter = max(0.0, ix2 - ix1) * max(0.0, iy2 - iy1)
    union = _area(box_a) + _area(box_b) - inter
    if union <= 0:
        return 0.0
    return inter / union


def nms(boxes, scores, iou_threshold) -> list:
    if len(boxes) != len(scores):
        raise ValueError("boxes and scores must have the same length")

    order = sorted(range(len(boxes)), key=lambda i: (-scores[i], i))
    kept = []
    for i in order:
        if all(iou(boxes[i], boxes[k]) <= iou_threshold for k in kept):
            kept.append(i)
    return kept
