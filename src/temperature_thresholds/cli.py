"""Main program defining command line interface."""

import argparse

from .main import anomalies
from .temperature_analysis import analyze_temperature_anomalies


def validate_thresholds(thresholds=None):
    """Validate that thresholds are within a range for  temperature anomalies."""
    if thresholds is None:
        thresholds = [1.5, 2.0]  # Default 

    valid_range = (-10, 10)
    for threshold in thresholds:
        if not valid_range[0] <= threshold <= valid_range[1]:
            raise ValueError(
                f"Threshold {threshold}°C is outside the plausible range {valid_range}. "
                "Please use realistic values for global temperature anomalies."
            )


def main():
    """Validate that thresholds are within a range for  temperature anomalies."""
    parser = argparse.ArgumentParser(
        description="Analyze temperature anomalies and generate exceedance reports."
    )
    parser.add_argument(
        "--info",
        action="store_true",
        help="Display information about the package and its functionality.",
    )
    parser.add_argument(
        "--exceedance",
        type=float,
        nargs="+",
        help="Temperature thresholds to analyze and display exceedance years.",
    )
    parser.add_argument(
        "--plot",
        type=float,
        nargs="+",
        help="Temperature thresholds to analyze and generate plots for (e.g., 1.5).",
    )
    args = parser.parse_args()

    if args.info:
        print(
            "This package analyzes global temperature anomalies using climate datasets."
            "It identifies when specific temperature thresholds are first exceeded and "
            "produces plots visualizing the anomalies."
        )
        return


    if args.exceedance:
        try:
            # from .main import anomalies
            validate_thresholds(args.exceedance)
            exceedance_years = analyze_temperature_anomalies(
                anomalies, args.exceedance, generate_plot=False
            )
            for threshold, year in exceedance_years.items():
                if year == "Not exceeded":
                    print(f"The threshold {threshold}°C was not exceeded.")
                else:
                    print(
                        f"The threshold {threshold}°C was first exceeded in the year {year}."
                    )
        except ValueError as e:
            print(e)
        return

    if args.plot:
        try:
            validate_thresholds(args.plot)
            analyze_temperature_anomalies(anomalies, args.plot, generate_plot=True)
            print(f"Plots generated for thresholds: {args.plot}")
        except ValueError as e:
            print(e)
        return


    print("Error: Please provide one of --info, --exceedance, or --plot arguments.")

    if __name__ == "__main__":
        main()
