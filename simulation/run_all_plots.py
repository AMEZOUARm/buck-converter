import sys
import os

# Ajouter la racine du projet au path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

print("\n" + "="*50)
print("  BUCK CONVERTER — Génération complète")
print("="*50)

print("\n[1/3] Simulation principale...")
from simulation.run_sim import main as run_main
run_main()

print("\n[2/3] Diagramme de Bode...")
from simulation.bode_plot import plot_bode
f_res = plot_bode()
print(f"  Fréquence de résonance : {f_res:.2f} Hz")

print("\n[3/3] Courbes de rendement...")
from simulation.efficiency_plot import plot_efficiency
loads, eta = plot_efficiency()
print(f"  Rendement max : {max(eta):.1f}%")

print("\n" + "="*50)
print("  Tous les graphiques sont dans assets/")
print("  simulation_results.png")
print("  bode_diagram.png")
print("  efficiency.png")
print("="*50 + "\n")