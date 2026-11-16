# Task 002 - Object dwell time from video detections

A video analytics system tracks objects across frames. Each detection is a tuple:

```python
(frame_index: int, track_id: int, label: str)
```

Write a Python function:

```python
def dwell_times(detections, fps) -> dict:
```

Return a dictionary `{track_id: seconds}` with how long each tracked object stayed in the scene.

Rules:

- An object's dwell time is `(last_frame - first_frame + 1) / fps`, rounded to 2 decimal places.
- Gaps between detections of the same object still count (the object is considered present from its first to its last frame).
- Detections can arrive in any order.
- The same `(frame_index, track_id)` may appear more than once; duplicates must not change the result.
- `label` is informational only and does not affect the result.
- `fps` must be a positive number; otherwise raise `ValueError`.
- An empty list of detections returns `{}`.
- Do not modify the input list.

Example:

```python
dwell_times([(0, 7, "person"), (29, 7, "person"), (10, 8, "car")], fps=30)
# {7: 1.0, 8: 0.03}
```

Write the solution in a single file `solution.py`.
