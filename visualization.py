import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE_DIR = "frontend"

def plot_flight_metrics(distance, fuel, carbon):
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    labels = ["Distance (km)", "Fuel (kg)", "Carbon (kg)"]
    values = [distance, fuel, carbon]

    
    plt.style.use("dark_background")

    fig, ax1 = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#0f172a")
    ax1.set_facecolor("#0f172a")

    bars = ax1.bar(labels, values, color="#76abff")

    ax1.set_title("Flight Route Performance Metrics", fontsize=16, pad=15)
    ax1.set_ylabel("Distance / Fuel / Carbon", fontsize=11)

    ax1.grid(axis="y", linestyle="--", alpha=0.3)
    ax1.spines["right"].set_visible(False)

    
    for b in bars:
        y = b.get_height()
        ax1.text(
            b.get_x() + b.get_width()/2,
            y,
            f"{y:,.2f}",
            ha="center",
            va="bottom",
            fontsize=10
        )

    plt.tight_layout()

    path = os.path.join(BASE_DIR, "metrics.png")
    plt.savefig(path, dpi=120)
    plt.close()
    return path
