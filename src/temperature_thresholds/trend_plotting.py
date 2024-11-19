"""trend_plotting.py."""

import matplotlib.pyplot as plt
from smoothing import apply_smoothing


def plot_trend(anomalies, smoothing_window=None, season="Annual"):
    """Plots the trend anomalies over time, with optional smoothing."""
    if smoothing_window:
        anomalies = apply_smoothing(anomalies, smoothing_window)

    global_trend_anomalies = anomalies.mean(dim=["lat", "lon"])


    plt.figure(figsize=(10, 6))
    global_trend_anomalies.plot(label=f"{season} Global Mean Anomaly")
    plt.title(
        f"{season} Global Temperature Trend Anomaly (relative to reference period)"
    )  # noqa: E501
    plt.xlabel("Year")
    plt.ylabel("Temperature Anomaly (°C)")
    if smoothing_window:
        plt.legend(title=f"Smoothed (Window = {smoothing_window} years)")
    plt.grid()
    plt.savefig("trend.png")
    plt.close()
