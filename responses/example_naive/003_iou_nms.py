# Hand-written "naive" answer used to demonstrate the evaluator.
# It is NOT output from a real model. Typical mistakes: divides by zero on
# zero-area boxes, suppresses boxes whose IoU equals the threshold, and does
# not check that boxes and scores have the same length.


def iou(box_a, box_b) -> float:
    ix1, iy1 = max(box_a[0], box_b[0]), max(box_a[1], box_b[1])
    ix2, iy2 = min(box_a[2], box_b[2]), min(box_a[3], box_b[3])
    inter = max(0, ix2 - ix1) * max(0, iy2 - iy1)
    area_a = (box_a[2] - box_a[0]) * (box_a[3] - box_a[1])
    area_b = (box_b[2] - box_b[0]) * (box_b[3] - box_b[1])
    return inter / (area_a + area_b - inter)


def nms(boxes, scores, iou_threshold) -> list:
    order = list(range(len(boxes)))
    order.sort(key=lambda i: scores[i], reverse=True)
    kept = []
    while order:
        best = order.pop(0)
        kept.append(best)
        order = [i for i in order if iou(boxes[best], boxes[i]) < iou_threshold]
    return kept
