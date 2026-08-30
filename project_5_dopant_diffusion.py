"""Project 5: constant-surface-concentration dopant diffusion into silicon."""

from __future__ import annotations

import csv
import os
import tempfile
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "cheme-matplotlib-cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import erfc


ROOT = Path(__file__).resolve().parent / "results" / "project_5_dopant_diffusion"


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    diffusivity, diffusion_time, surface_concentration = 1e-13, 3600.0, 1e20
    depth_cm = np.linspace(0, 1e-4, 501)
    depth_um = depth_cm * 1e4
    concentration = surface_concentration * erfc(
        depth_cm / (2 * np.sqrt(diffusivity * diffusion_time))
    )
    threshold = 1e18
    junction_um = float(np.interp(np.log10(threshold), np.log10(concentration[::-1]), depth_um[::-1]))

    with (ROOT / "project_5_dopant_diffusion_data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["depth_um", "dopant_concentration_atoms_cm3"])
        writer.writerows(zip(depth_um, concentration))

    fig, ax = plt.subplots(figsize=(8.4, 5))
    ax.semilogy(depth_um, concentration, color="#6A4C93", linewidth=2.8)
    ax.axhline(threshold, color="#E76F51", linestyle="--", linewidth=1.8,
               label="Reference threshold = 1e18 atoms/cm^3")
    ax.axvline(junction_um, color="#E9C46A", linestyle=":", linewidth=2.2,
               label=f"Junction depth = {junction_um:.3f} um")
    ax.set(title="Dopant Diffusion Profile in Silicon", xlabel="Depth into wafer (um)",
           ylabel="Dopant concentration (atoms/cm^3)")
    ax.grid(True, alpha=0.22)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(ROOT / "project_5_dopant_diffusion_plot.png", dpi=180,
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Junction depth at 1e18 atoms/cm^3: {junction_um:.3f} um")
    print(f"Saved results to {ROOT}")


if __name__ == "__main__":
    main()


