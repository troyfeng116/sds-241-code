import random
import statistics

from tqdm import tqdm
from typing import Callable, Optional, Tuple


def choose_point(
    x_bd: Optional[Tuple[int, int]] = (0, 1), y_bd: Optional[Tuple[int, int]] = (0, 1)
) -> Tuple[float, float]:
    x_min, x_max = x_bd
    y_min, y_max = y_bd
    return x_min + random.random() * (x_max - x_min), y_min + random.random() * (
        y_max - y_min
    )


def run_sample(fn: Callable[[], bool], trials: int) -> float:
    ct = 0
    for _ in range(trials):
        ct += 1 if fn() else 0
    return ct / trials


def run_sims_and_report(
    fn: Callable[[], bool],
    sample_size: Optional[int] = 100,
    trials_per_sample: Optional[int] = 100,
    sample_res_map: Optional[Callable[[float], float]] = lambda x: x,
):
    """Run `samples` rounds of `trials` trials of `fn`, compute + report sample aggregate statistics.

    Args:
        fn (Callable[[], bool]): Single experiment trial runnable; return `True` iff success.
        samples (Optional[int], optional): Size of sample. Defaults to 100.
        trials (Optional[int], optional): Number of trials to run per sample. Defaults to 100.
        sample_res_map (Optional[Callable[[float], float]], optional): Additional map to apply to each sample result. Defaults to identity.
    """
    sample_results = []
    for _ in tqdm(range(sample_size)):
        sample_results.append(
            sample_res_map(run_sample(fn=fn, trials=trials_per_sample))
        )

    print(
        f"mean={statistics.mean(sample_results)}, stdev={statistics.stdev(sample_results)}"
    )