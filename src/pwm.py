import numpy as np

class PWMGenerator:
    """
    Générateur de signal PWM.
    Produit un signal carré à fréquence et duty cycle variables.
    """

    def __init__(self, frequency, timestep):
        self.fsw = frequency
        self.dt  = timestep
        self.T   = 1.0 / frequency  # Période PWM

    def signal(self, t, duty_cycle):
        """
        Retourne 1 (ON) ou 0 (OFF) à l'instant t
        selon le duty cycle D.
        """
        phase = (t % self.T) / self.T
        return 1.0 if phase < duty_cycle else 0.0

    def generate_waveform(self, time_array, duty_cycle):
        """
        Génère le vecteur PWM complet sur time_array.
        duty_cycle : float fixe ou tableau numpy de même taille.
        """
        if np.isscalar(duty_cycle):
            return np.array([self.signal(t, duty_cycle) for t in time_array])
        else:
            return np.array([
                self.signal(t, d)
                for t, d in zip(time_array, duty_cycle)
            ])

    def duty_to_voltage(self, duty_cycle, Vin):
        """Tension de sortie moyenne théorique."""
        return duty_cycle * Vin