"""Generic dimensionless grammar, determined only by the public input domain."""
from dataclasses import dataclass
import numpy as np


@dataclass
class Library:
    powers: list
    scale: np.ndarray

    @classmethod
    def build(cls, bounds, probes):
        low = -1 if np.all(bounds[:, 0] > 0) else 0
        powers = [(a, b) for a in range(low, 4) for b in range(low, 4)
                  if abs(a)+abs(b) <= 3]
        powers.sort(key=lambda p: (abs(p[0])+abs(p[1]), p))
        raw = cls(powers, np.ones(len(powers)))
        raw.scale = np.maximum(np.sqrt(np.mean(raw.transform(probes)**2, axis=0)), 1e-8)
        return raw

    def transform(self, x):
        with np.errstate(divide='raise', invalid='raise', over='raise'):
            values = np.column_stack([x[:, 0]**a*x[:, 1]**b for a, b in self.powers])
        if not np.isfinite(values).all():
            raise ValueError('nonfinite features')
        return values / self.scale

    def expression(self, c):
        terms = []
        for value, scale, (a, b) in zip(c, self.scale, self.powers):
            if abs(value) > 1e-10:
                terms.append(f'({value/scale:.12g})*x0**({a})*x1**({b})')
        return ' + '.join(terms) or '0'

    def symbolic(self, c, tolerance=1e-6):
        import sympy as sp
        x0, x1 = sp.symbols('x0 x1')
        return sum(sp.Rational(str(round(float(v/s), 6)))*x0**a*x1**b
                   for v, s, (a, b) in zip(c, self.scale, self.powers) if abs(v/s) >= tolerance)
