"""The entire numerical learner interface; no task names or hidden labels."""
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class Observations:
    x: np.ndarray
    y: np.ndarray
    calibration_x: np.ndarray
    calibration_y: np.ndarray
    acquired_x: np.ndarray
    acquired_y: np.ndarray
    pool: np.ndarray
    probes: np.ndarray
    bounds: np.ndarray
    noise_std: float
    output_scale: float = 1.0

    def __post_init__(self):
        for x, y in ((self.x, self.y), (self.calibration_x, self.calibration_y),
                     (self.acquired_x, self.acquired_y)):
            if x.ndim != 2 or x.shape[1] != 2 or y.shape != (len(x),):
                raise ValueError('inconsistent observation shapes')
            if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
                raise ValueError('nonfinite observations')
        if self.noise_std < 0 or self.output_scale <= 0:
            raise ValueError('invalid declared scale')
