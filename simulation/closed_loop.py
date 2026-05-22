import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.buck_model import BuckConverter, load_config
from src.pi_controller import PIController
from src.utils import compute_ripple, compute_efficiency, settling_time

def run_closed_loop(config=None):
    """
    Simulation boucle fermée : PI contrôle le duty cycle
    pour maintenir Vout = 12V malgré les perturbations.
    """
    cfg    = config or load_config()
    buck   = BuckConverter(cfg)
    pi_cfg = cfg['pi_controller']

    pi = PIController(
        kp=pi_cfg['kp'],
        ki=pi_cfg['ki'],
        output_min=pi_cfg['output_min'],
        output_max=pi_cfg['output_max']
    )

    # Vecteurs résultats
    n      = buck.n_steps
    Vout   = np.zeros(n)
    iL     = np.zeros(n)
    duty   = np.zeros(n)
    error  = np.zeros(n)

    # Conditions initiales
    vout_k = 0.0
    iL_k   = 0.0
    duty[0] = cfg['converter']['duty_cycle']

    for k in range(1, n):
        # Contrôleur PI calcule le duty cycle
        D = pi.compute(
            setpoint=buck.Vout_target,
            measured=vout_k,
            dt=buck.dt
        )

        # Modèle Buck : équations d'état
        diL, dV = buck.derivatives(iL_k, vout_k, D)
        iL_k   += diL * buck.dt
        vout_k += dV  * buck.dt

        # Sécurité physique
        iL_k   = max(iL_k, 0.0)
        vout_k = max(vout_k, 0.0)

        # Stockage
        Vout[k]  = vout_k
        iL[k]    = iL_k
        duty[k]  = D
        error[k] = buck.Vout_target - vout_k

    # Calcul métriques régime permanent
    steady_idx = int(cfg['simulation']['steady_state'] / buck.dt)
    ripple_v   = compute_ripple(Vout, steady_idx)
    ripple_i   = compute_ripple(iL, steady_idx)
    eta        = compute_efficiency(buck.Vin, np.mean(Vout[steady_idx:]),
                                    iL[steady_idx:], buck.R)
    t_settle   = settling_time(buck.time, Vout, buck.Vout_target)

    stats = {
        'Vout_moyen (V)':      round(float(np.mean(Vout[steady_idx:])), 4),
        'Ripple tension (V)':  ripple_v,
        'Courant moyen (A)':   round(float(np.mean(iL[steady_idx:])), 4),
        'Ripple courant (A)':  ripple_i,
        'Rendement η (%)':     eta,
        'Temps réponse (s)':   t_settle,
        'Duty final (%)':      round(float(duty[-1]) * 100, 2)
    }

    return buck.time, Vout, iL, duty, error, stats