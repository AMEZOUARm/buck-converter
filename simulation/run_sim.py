import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from src.buck_model import load_config
from src.utils import print_summary
from simulation.open_loop import run_open_loop
from simulation.closed_loop import run_closed_loop

def plot_results(time, Vout_ol, Vout_cl, iL_ol, iL_cl, duty, error):
    """Génère les 4 graphiques professionnels."""

    fig = plt.figure(figsize=(14, 10))
    fig.suptitle('Convertisseur Buck DC-DC  —  24V → 12V',
                 fontsize=15, fontweight='bold', y=0.98)

    gs = gridspec.GridSpec(2, 2, hspace=0.45, wspace=0.35)

    # Couleurs
    C_OL  = '#5F8DD3'   # boucle ouverte — bleu
    C_CL  = '#2ECC71'   # boucle fermée  — vert
    C_REF = '#E74C3C'   # référence      — rouge
    C_DUT = '#F39C12'   # duty cycle     — orange

    # ── Graphique 1 : Tension de sortie ──────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(time * 1e3, Vout_ol, color=C_OL, linewidth=1.2,
             label='Boucle ouverte', alpha=0.8)
    ax1.plot(time * 1e3, Vout_cl, color=C_CL, linewidth=1.5,
             label='Boucle fermée (PI)')
    ax1.axhline(12.0, color=C_REF, linewidth=1,
                linestyle='--', label='Référence 12V')
    ax1.set_title('Tension de sortie Vout')
    ax1.set_xlabel('Temps (ms)')
    ax1.set_ylabel('Tension (V)')
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-1, 16)

    # ── Graphique 2 : Courant dans l'inductance ───────────────
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(time * 1e3, iL_ol, color=C_OL, linewidth=1.2,
             label='Boucle ouverte', alpha=0.8)
    ax2.plot(time * 1e3, iL_cl, color=C_CL, linewidth=1.5,
             label='Boucle fermée (PI)')
    ax2.set_title('Courant inductance iL')
    ax2.set_xlabel('Temps (ms)')
    ax2.set_ylabel('Courant (A)')
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)

    # ── Graphique 3 : Duty cycle PI ───────────────────────────
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(time * 1e3, duty * 100, color=C_DUT, linewidth=1.2)
    ax3.axhline(50.0, color=C_REF, linewidth=1,
                linestyle='--', label='D théorique 50%')
    ax3.set_title('Duty cycle — Sortie PI')
    ax3.set_xlabel('Temps (ms)')
    ax3.set_ylabel('Duty cycle (%)')
    ax3.legend(fontsize=8)
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(0, 100)

    # ── Graphique 4 : Erreur de régulation ───────────────────
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.plot(time * 1e3, error, color=C_REF, linewidth=1.2)
    ax4.axhline(0, color='gray', linewidth=0.8, linestyle='--')
    ax4.set_title('Erreur de régulation')
    ax4.set_xlabel('Temps (ms)')
    ax4.set_ylabel('Erreur (V)')
    ax4.grid(True, alpha=0.3)

    # Sauvegarde
    os.makedirs('assets', exist_ok=True)
    path = os.path.join('assets', 'simulation_results.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    print(f"\n  Graphique sauvegardé : {path}")
    plt.show()

def main():
    print("\n  Chargement configuration...")
    cfg = load_config()

    print("  Simulation boucle ouverte...")
    time, Vout_ol, iL_ol, stats_ol = run_open_loop(cfg)
    print_summary(stats_ol)

    print("  Simulation boucle fermée (PI)...")
    time, Vout_cl, iL_cl, duty, error, stats_cl = run_closed_loop(cfg)
    print_summary(stats_cl)

    print("  Génération des graphiques...")
    plot_results(time, Vout_ol, Vout_cl, iL_ol, iL_cl, duty, error)

if __name__ == '__main__':
    main()