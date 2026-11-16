def dwell_times(detections, fps) -> dict:
    if isinstance(fps, bool) or not isinstance(fps, (int, float)) or fps <= 0:
        raise ValueError("fps must be a positive number")

    spans = {}
    for frame, track_id, _label in detections:
        if track_id in spans:
            first, last = spans[track_id]
            spans[track_id] = (min(first, frame), max(last, frame))
        else:
            spans[track_id] = (frame, frame)

    return {tid: round((last - first + 1) / fps, 2) for tid, (first, last) in spans.items()}
