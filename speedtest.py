"""

============
speedtest.py
============

"""

import os
import argparse
import subprocess

import datetime

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

def error_entry():
    return ",".join([
        "-1",
        "N/A",
        "N/A",
        datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat() + "Z",
        "nan",
        "nan",
        "0",
        "0",
        "nan",
        "N/A",
    ]) + "\n"

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
    entry = result.stdout.decode("utf-8")[:-1]
    if not entry:
        entry = error_entry()
    with open(data_filename, "a") as dfile:
        dfile.write(entry)


if __name__ == "__main__":
    ARGS = ARG_PARSER.parse_args()
    main(ARGS.data_filename)
