import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import matplotlib.pyplot as plt
from src.buck_model import BuckConverter, load_config

def plot_efficiency(save=True):
    """
    Trace le rendement η en fonction de la résistance de charge.
    Plus R est faible = plus de courant = plus de pertes.
    """
    cfg    = load_config()
    loads  = np.linspace(2, 50, 50)   # R de 2Ω à 50Ω
    eta    = []
    vout   = []

    for R in loads:
        cfg['components']['resistance'] = float(R)
        buck = BuckConverter(cfg)
        _, iL, Vout = buck.run_open_loop()

        steady = int(cfg['simulation']['steady_state'] / buck.dt)
        V_mean = np.mean(Vout[steady:])
        I_mean = np.mean(iL[steady:])
        Pin    = buck.Vin * I_mean
        Pout   = V_mean**2 / R
        e      = (Pout / Pin * 100) if Pin > 0 else 0
        eta.append(round(e, 2))
        vout.append(round(V_mean, 3))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('Analyse rendement — Buck 24V→12V',
                 fontsize=13, fontweight='bold')

    # Rendement vs charge
    ax1.plot(loads, eta, color='#2ECC71', linewidth=2, marker='o',
             markersize=3)
    ax1.axhline(max(eta), color='#E74C3C', linestyle='--',
                linewidth=1, label=f'η max = {max(eta):.1f}%')
    ax1.set_xlabel('Résistance de charge (Ω)')
    ax1.set_ylabel('Rendement η (%)')
    ax1.set_title('Rendement vs charge')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 110)

    # Vout vs charge
    ax2.plot(loads, vout, color='#3498DB', linewidth=2, marker='s',
             markersize=3)
    ax2.axhline(12.0, color='#E74C3C', linestyle='--',
                linewidth=1, label='Cible 12V')
    ax2.set_xlabel('Résistance de charge (Ω)')
    ax2.set_ylabel('Tension sortie (V)')
    ax2.set_title('Régulation tension vs charge')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    if save:
        os.makedirs('assets', exist_ok=True)
        path = os.path.join('assets', 'efficiency.png')
        plt.savefig(path, dpi=150, bbox_inches='tight')
        print(f"  Rendement sauvegardé : {path}")

    plt.show()
    return loads, eta