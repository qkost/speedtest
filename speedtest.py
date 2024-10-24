"""

============
speedtest.py
============

"""

import os
import argparse
import subprocess

ARG_PARSER = argparse.ArgumentParser(description="Script for internet speed test.")

ARG_PARSER.add_argument(
    "--data_filename",
    "-d",
    type=str,
    help="Filename to save data",
    default=os.path.join(os.path.dirname(__file__), "data.csv")
)
SPEEDTEST_FILENAME = "data.csv"
"""
Default speedtest data file.
"""

def main(data_filename):
    """
    Perform speedtest and append the results to the speedtest data file.
    
    Parameters
    ----------
    data_filename : str
        Name of CSV file to save data to
    """

    if not os.path.exists(data_filename):
        result = subprocess.run(["speedtest-cli", "--csv-header"], capture_output=True)
        with open(data_filename, "w") as dfile:
            dfile.write(result.stdout.decode("utf-8")[:-1])

    result = subprocess.run(["speedtest-cli", "--csv"], capture_output=True)
    breakpoint
    with open(data_filename, "a") as dfile:
        dfile.write(result.stdout.decode("utf-8")[:-1])


if __name__ == "__main__":
    ARGS = ARG_PARSER.parse_args()
    main(ARGS.data_filename)
