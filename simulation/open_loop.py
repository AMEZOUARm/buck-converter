import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.buck_model import BuckConverter, load_config
from src.utils import compute_ripple, compute_efficiency, settling_time
import numpy as np

def run_open_loop(config=None):
    """
    Simulation boucle ouverte — duty cycle fixe à 0.5.
    Sert de référence pour comparer avec la boucle fermée.
    """
    cfg  = config or load_config()
    buck = BuckConverter(cfg)

    time, iL, Vout = buck.run_open_loop()

    steady_idx = int(cfg['simulation']['steady_state'] / buck.dt)
    ripple_v   = compute_ripple(Vout, steady_idx)
    eta        = compute_efficiency(buck.Vin, np.mean(Vout[steady_idx:]),
                                    iL[steady_idx:], buck.R)

    stats = {
        'Vout_moyen (V)':     round(float(np.mean(Vout[steady_idx:])), 4),
        'Ripple tension (V)': ripple_v,
        'Rendement η (%)':    eta,
        'Duty cycle fixe (%)': round(cfg['converter']['duty_cycle'] * 100, 2)
    }

    return time, Vout, iL, stats