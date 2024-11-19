"""main.py."""
import xarray as xr

# File paths
file1= "src/temperature_thresholds/data/ssp85.nc"
file2= "src/temperature_thresholds/data/historical.nc"


def calculate_anomalies(historical_file, ssp_file):
    """Calculate temperature anomalies based on historical and SSP data."""
    historical_data = xr.open_dataset(historical_file)
    ssp585_data = xr.open_dataset(ssp_file)

    temperature_historical = historical_data["tas"]
    temperature_ssp585 = ssp585_data["tas"]

    temperature_historical_celsius = temperature_historical - 273.15
    temperature_ssp585_celsius = temperature_ssp585 - 273.15

    ref_period = temperature_historical_celsius.sel(
        time=slice("1850-01-01", "1900-12-31")
    )

    ref_mean = ref_period.groupby("time.year").mean("time").mean(["year", "lat", "lon"])

    yearly_global_historical = (
        temperature_historical_celsius.groupby("time.year")
        .mean("time")
        .mean(dim=["lat", "lon"])
    )
    yearly_global_ssp585 = (
        temperature_ssp585_celsius.groupby("time.year")
        .mean("time")
        .mean(dim=["lat", "lon"])
    )


    yearly_g_mean = xr.concat(
        [yearly_global_historical, yearly_global_ssp585], dim="year"
    )

    anomalies = yearly_g_mean - ref_mean

    anomalies = anomalies.to_dataset(name="tas")

    return anomalies



# Export the anomalies
anomalies = calculate_anomalies(file2, file1)
