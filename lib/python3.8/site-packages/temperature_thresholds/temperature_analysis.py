"""analyzes temperatute."""

import matplotlib.pyplot as plt


def analyze_temperature_anomalies(anomalies, thresholds, generate_plot=True):
    """Analyzes temperature anomalies and finds years when  thresholds are exceeded."""
    exceedance_years = {}

    for threshold in thresholds:
        threshold_exceedance = anomalies.where(anomalies >= threshold, drop=True)
        first_exceedance_year = (
            threshold_exceedance.year[0].values
            if len(threshold_exceedance.year) > 0
            else "Not exceeded"
        )
        exceedance_years[threshold] = first_exceedance_year

    if generate_plot:
        # Anomalies plot
        plt.figure(figsize=(12, 6))
        # anomalies.plot(label="Temperature Anomalies (°C)")
        anomalies["tas"].plot(label="Temperature Anomalies (°C)")
        for threshold in thresholds:
            plt.axhline(threshold, linestyle="--", label=f"{threshold}°C Threshold")

        if exceedance_years[threshold] != "Not exceeded":
            plt.axvline(
                exceedance_years[threshold],
                linestyle=":",
                label=f"First >{threshold}°C in {exceedance_years[threshold]}",
            )

            plt.title(
                "Yearly Global Mean Temperature Anomalies (1850-2100) and Thresholds"
            )
            plt.xlabel("Year")
            plt.ylabel("Temperature Anomaly (°C)")
            plt.legend()
            plt.grid()
            plt.savefig("temperature_anomaliesplot.png")
            plt.close()

    return exceedance_years
