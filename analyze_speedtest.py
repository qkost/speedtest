"""

====================
analyze_speedtest.py
====================

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from speedtest import ARG_PARSER

ARG_PARSER.add_argument(
    "--rolling_duration",
    "-r",
    type=str,
    help="Rolling window duration",
    default="1d"
)

def main(data_filename, window):
    """
    Analyze speedtest data.
    
    Parameters
    ----------
    data_filename : str
        Name of CSV file containing speedtest results
    """

    # Load data
    df = pd.read_csv(data_filename)

    # Convert to date
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df = df.set_index("Timestamp")
    df["Success"] = (df["Server ID"] != -1)

    # Convert units
    df["Download"] /= 1e6
    df["Upload"] /= 1e6
    df_fails = df[~df["Success"]]

    # Create rolling average
    rolling = df.rolling(window).mean()

    # Range of data (for titles)
    start_date, stop_date = [
        dstr.strftime("%Y-%m-%d")
        for dstr in (df.index[0], df.index[-1])
    ]
    date_range_str = f"{start_date} to {stop_date}"

    # Timeseries data
    columns = ["Download", "Upload", "Ping"]
    fig, axes = plt.subplots(
        len(columns),
        1,
        sharex=True,
        figsize=0.8 * np.array([16, 9])
    )
    for ax, column in zip(axes, columns):
        ax.plot(rolling.index, rolling[column], marker=".", linestyle="None")
        for fail_date in df_fails.index:
            ax.axvline(fail_date, color="C3", linestyle="-", linewidth=0.5)
        ax.set_ylabel(column)
        ax.grid()
    axes[0].set_title(f"Internet Speed for {date_range_str}\nRolling Window: {window}")
    fig.tight_layout()

    # Histograms
    for column in columns:
        fig, ax = plt.subplots(figsize=0.8 * np.array([16, 9]))
        ax.hist(df[column], bins=100, histtype="step", density=True)
        ax.set_xlabel(column)
        ax.set_ylabel("PDF")
        ax.set_title(f"Internet Speed for {date_range_str}")
        ax.grid()
        fig.tight_layout()

    # Percent downtime
    # Note that I added the ability for speedtest.py to record failed tests later on
    # So we only want to consider times after the first failed test
    if not df_fails.empty:
        first_failed_test = df_fails.index[0]
        df_post_fail = df[first_failed_test:]

        # Range of data -- this is only for after the first failed test
        start_date, stop_date = [
            dstr.strftime("%Y-%m-%d")
            for dstr in (df_post_fail.index[0], df_post_fail.index[-1])
        ]
        date_range_str = f"{start_date} to {stop_date}"

        fig, ax = plt.subplots(figsize=0.8 * np.array([16, 9]))
        counts = df_post_fail["Success"].value_counts()
        counts.sort_values().plot(kind = "bar", ax=ax)
        ax.set_ylabel("Count")
        ax.set_title(
            f"Speedtest Successful Counts for {date_range_str}\n"
            f"Uptime: {counts[True]/counts.sum() * 100:.1f}%"
        )
        ax.grid()
        fig.tight_layout()

if __name__ == "__main__":
    ARGS = ARG_PARSER.parse_args()
    main(ARGS.data_filename, ARGS.rolling_duration)
    plt.show()