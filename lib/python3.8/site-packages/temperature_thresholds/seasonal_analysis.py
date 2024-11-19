"""seasonal analysis."""
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import xarray as xr


def _compute_season_mean(data, months, dim="time"):
    """Computes seasonal mean for specified months."""
    season_data = data.where(data[dim + ".month"].isin(months), drop=True)
    season_mean = season_data.groupby(f"{dim}.year").mean(dim)
    return season_mean


def compute_seasonal_anomalies(
    temperature_data, reference_period=("1850-01-01", "1900-12-31")
):
    """Computes seasonal temperature anomalies for DJF, MAM, JJA, and SON."""
    seasons = {
        "DJF": [12, 1, 2],
        "MAM": [3, 4, 5],
        "JJA": [6, 7, 8],
        "SON": [9, 10, 11],
    }

    # Calculate reference seasonal averages
    reference_data = temperature_data.sel(time=slice(*reference_period))
    seasonal_reference_means = {
        season: _compute_season_mean(reference_data, months).mean("year")
        for season, months in seasons.items()
    }

    # Calculate anomalies for all seasons
    seasonal_anomalies = {}
    global_mean_anomalies = {}
    for season, months in seasons.items():
        season_mean = _compute_season_mean(temperature_data, months)
        anomalies = season_mean - seasonal_reference_means[season]
        seasonal_anomalies[season] = anomalies
        global_mean_anomalies[season] = anomalies.mean(dim=["lat", "lon"])

    # Combine anomalies for all seasons into a single dataset
    combined_seasonal_anomalies = xr.Dataset(seasonal_anomalies)
    combined_global_mean_anomalies = xr.Dataset(global_mean_anomalies)
    return combined_seasonal_anomalies, combined_global_mean_anomalies


def find_threshold_exceedance(global_mean_anomalies, thresholds):
    """Finds the first year each season's anomaly exceeds the thresholds."""
    exceedance_years = {threshold: {} for threshold in thresholds}

    for threshold in thresholds:
        for season, anomalies in global_mean_anomalies.items():
            exceedance = anomalies > threshold
            if exceedance.any():
                year_idx = int(anomalies["year"][exceedance.argmax()].values)
                exceedance_years[threshold][season] = year_idx
            else:
                exceedance_years[threshold][season] = "Not exceeded"

    return exceedance_years


def plot_regional_anomalies(
    seasonal_anomalies, threshold, season, year, vmin=-2, vmax=2
):
    """Plots regional temperature anomalies."""
    anomaly_data = seasonal_anomalies[season].sel(year=year)

    # Set up the plot with a projection
    fig, ax = plt.subplots(
        figsize=(10, 6), subplot_kw={"projection": ccrs.PlateCarree()}
    )

    # Plot the anomaly data
    anomaly_data.plot(
        ax=ax,
        cmap="coolwarm",
        vmin=vmin,
        vmax=vmax,
        cbar_kwargs={"label": "Temperature Anomaly (°C)"},
        transform=ccrs.PlateCarree(),
    )

    # Add map features
    features = [
        cfeature.COASTLINE,
        cfeature.BORDERS,
        cfeature.LAND.with_scale("50m"),
        cfeature.OCEAN.with_scale("50m"),
        cfeature.LAKES,
        cfeature.RIVERS,
    ]
    for feature in features:
        ax.add_feature(feature, edgecolor="black")

    ax.set_title(f"{season} Temperature Anomalies in {year} (Threshold: {threshold}°C)")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    # Save the figure
    plt.savefig(
        f"{season}_temperature_anomalies_{year}_{threshold}C.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()
