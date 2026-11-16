# Mini Coding Benchmark

A small, original benchmark for evaluating how well LLMs write correct Python code.
Each task has a clear prompt, a reference solution and hidden tests that focus on
edge cases where models usually fail. A small evaluator runs any model's answers in
an isolated folder and records the results.

The tasks come from real computer-vision and video-analytics work:

| Task | What the model must write | Edge cases tested |
| --- | --- | --- |
| [001_brazilian_plate](tasks/001_brazilian_plate/prompt.md) | Validator for old and Mercosul Brazilian license plates | lowercase, hyphen position, spaces, accented letters, full-width digits, non-string input |
| [002_dwell_time](tasks/002_dwell_time/prompt.md) | Time each tracked object stays in a video scene | unordered input, gaps, duplicates, float FPS, invalid FPS, input mutation |
| [003_iou_nms](tasks/003_iou_nms/prompt.md) | IoU between boxes and greedy Non-Maximum Suppression | touching edges, zero-area boxes, score ties, threshold equality, input mutation |

## Structure

```text
tasks/<task_id>/
  prompt.md        # what the model receives
  reference.py     # correct solution (proves the task is solvable)
  test_hidden.py   # pytest tests the model never sees
responses/<model>/
  <task_id>.py     # one answer file per task
run_eval.py        # runs answers against hidden tests, prints pass@1, appends results.csv
```

## How to run

```bash
pip install -r requirements.txt

# 1. Sanity check: every reference solution must pass (also runs in CI)
python run_eval.py --reference

# 2. Evaluate a model
#    Paste each prompt.md into the model, save its code as responses/<model>/<task_id>.py
python run_eval.py responses/<model>
```

Each answer is copied to a temporary folder as `solution.py` together with the hidden
tests, then pytest runs with a 60-second timeout. The script reports how many tests
passed per task, the first failure message, and the overall pass@1.

## Example output

`responses/example_naive` holds **hand-written** answers with common mistakes (they are
not real model output). They show what the hidden tests catch:

```text
[FAIL] 001_brazilian_plate: 14/22 tests  -> test_invalid[ABC12D3]: AssertionError: assert True is False
[FAIL] 002_dwell_time: 2/14 tests  -> test_example_from_prompt: assert {7: 0.97, 8: 0.0} == {7: 1.0, 8: 0.03}
[FAIL] 003_iou_nms: 13/16 tests  -> test_zero_area_boxes_do_not_divide_by_zero: ZeroDivisionError: division by zero

example_naive: pass@1 = 0/3 tasks (0%)
```

## Design principles

1. **Unambiguous prompts** - every rule the tests check is written in the prompt.
2. **Test behavior, not implementation** - any correct approach passes.
3. **Edge cases first** - empty input, invalid types, ties, boundaries, side effects.
4. **Deterministic** - no network, clock or randomness.
5. **Original tasks** - not copied from public problem sets, to reduce contamination.
6. **Validated** - CI fails if a reference solution does not pass its own tests.

## Adding a task

1. Create `tasks/<NNN_name>/` with `prompt.md`, `reference.py` and `test_hidden.py`.
2. Run `python run_eval.py --reference` and make sure it passes.
3. Collect model answers in `responses/<model>/` and run the evaluator.
