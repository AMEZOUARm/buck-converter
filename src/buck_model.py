import numpy as np
import yaml
import os

def load_config(path=None):
    if path is None:
        path = os.path.join(os.path.dirname(__file__),
                            '..', 'simulation', 'config.yaml')
    with open(path, 'r') as f:
        return yaml.safe_load(f)

class BuckConverter:
    """
    Modèle du convertisseur Buck DC-DC.
    Équations d'état :
      diL/dt = (Vin * D - Vout) / L
      dVout/dt = (iL - Vout / R) / C
    """

    def __init__(self, config=None):
        cfg = config or load_config()
        c = cfg['converter']
        comp = cfg['components']
        sim = cfg['simulation']

        self.Vin   = c['vin']
        self.Vout_target = c['vout']
        self.D     = c['duty_cycle']
        self.fsw   = c['frequency']

        self.L     = comp['inductance']
        self.C     = comp['capacitance']
        self.R     = comp['resistance']
        self.ESR   = comp['esr']

        self.dt    = sim['timestep']
        self.T_sim = sim['duration']

        # Vecteurs de résultats
        self.n_steps = int(self.T_sim / self.dt)
        self.time    = np.linspace(0, self.T_sim, self.n_steps)
        self.iL      = np.zeros(self.n_steps)   # Courant inductance
        self.Vout    = np.zeros(self.n_steps)    # Tension sortie

    def derivatives(self, iL, Vout, D):
        """Calcule diL/dt et dVout/dt."""
        diL_dt   = (self.Vin * D - Vout) / self.L
        dVout_dt = (iL - Vout / self.R) / self.C
        return diL_dt, dVout_dt

    def run_open_loop(self, D=None):
        """Simulation boucle ouverte — duty cycle fixe."""
        D = D or self.D
        iL, Vout = 0.0, 0.0

        for k in range(1, self.n_steps):
            diL, dV = self.derivatives(iL, Vout, D)
            # Intégration Euler explicite
            iL   += diL * self.dt
            Vout += dV  * self.dt
            # Sécurité : pas de tension négative
            Vout = max(Vout, 0.0)
            iL   = max(iL, 0.0)
            self.iL[k]   = iL
            self.Vout[k] = Vout

        return self.time, self.iL, self.Vout

    def steady_state_values(self):
        """Valeurs théoriques en régime permanent."""
        Vout_th = self.Vin * self.D
        iL_th   = Vout_th / self.R
        ripple_V = (Vout_th * (1 - self.D)) / (8 * self.L * self.C * self.fsw**2)
        ripple_I = (self.Vin - Vout_th) * self.D / (self.L * self.fsw)
        return {
            'Vout_theorique': round(Vout_th, 4),
            'iL_theorique':   round(iL_th, 4),
            'ripple_tension': round(ripple_V, 6),
            'ripple_courant': round(ripple_I, 4),
            'rendement_ideal': round((Vout_th / self.Vin) * 100, 2)
        }