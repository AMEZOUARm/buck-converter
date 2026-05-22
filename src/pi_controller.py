import numpy as np

class PIController:
    """
    Régulateur PI numérique avec anti-windup.
    
    u(t) = Kp * e(t) + Ki * integral(e(t))
    
    Anti-windup : on gèle l'intégrale si la sortie
    est saturée (duty cycle min/max atteint).
    """

    def __init__(self, kp, ki, output_min=0.1, output_max=0.9):
        self.Kp  = kp
        self.Ki  = ki
        self.out_min = output_min
        self.out_max = output_max

        # États internes
        self._integral   = 0.0
        self._prev_error = 0.0
        self._saturated  = False

    def reset(self):
        """Remet le contrôleur à zéro."""
        self._integral   = 0.0
        self._prev_error = 0.0
        self._saturated  = False

    def compute(self, setpoint, measured, dt):
        """
        Calcule la nouvelle commande (duty cycle).
        
        Args:
            setpoint : tension cible (V)
            measured : tension mesurée (V)
            dt       : pas de temps (s)
        Returns:
            duty_cycle clampé entre out_min et out_max
        """
        error = setpoint - measured

        # Anti-windup : intégration uniquement si pas saturé
        if not self._saturated:
            self._integral += error * dt

        # Calcul PI
        u = self.Kp * error + self.Ki * self._integral

        # Saturation + détection
        u_clamped = np.clip(u, self.out_min, self.out_max)
        self._saturated = (u != u_clamped)

        self._prev_error = error
        return u_clamped

    def get_state(self):
        """Retourne l'état interne du contrôleur."""
        return {
            'integral':   round(self._integral, 6),
            'prev_error': round(self._prev_error, 6),
            'saturated':  self._saturated
        }