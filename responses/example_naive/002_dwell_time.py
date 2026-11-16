# Hand-written "naive" answer used to demonstrate the evaluator.
# It is NOT output from a real model. Typical mistakes: assumes detections are
# sorted, forgets the "+1 frame", and does not validate fps.


def dwell_times(detections, fps) -> dict:
    result = {}
    first_seen = {}
    for frame, track_id, _ in detections:
        if track_id not in first_seen:
            first_seen[track_id] = frame
        result[track_id] = round((frame - first_seen[track_id]) / fps, 2)
    return result
