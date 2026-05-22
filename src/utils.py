import numpy as np

def compute_efficiency(Vin, Vout, iL, R):
    """Calcule le rendement η du convertisseur."""
    Pin  = Vin * np.mean(iL)
    Pout = (Vout**2) / R
    if Pin <= 0:
        return 0.0
    return round((Pout / Pin) * 100, 2)

def compute_ripple(signal, start_idx):
    """
    Calcule l'ondulation pic-à-pic
    sur la portion steady-state du signal.
    """
    steady = signal[start_idx:]
    return round(np.max(steady) - np.min(steady), 6)

def settling_time(time, signal, target, tolerance=0.02):
    """
    Temps de réponse à ±2% de la valeur cible.
    """
    band = tolerance * target
    for i in range(len(signal) - 1, -1, -1):
        if abs(signal[i] - target) > band:
            return round(time[i], 6)
    return 0.0

def print_summary(stats: dict):
    """Affiche un résumé formaté des résultats."""
    print("\n" + "="*45)
    print("   RÉSULTATS — Convertisseur Buck 24V→12V")
    print("="*45)
    for key, val in stats.items():
        print(f"  {key:<25} : {val}")
    print("="*45 + "\n")