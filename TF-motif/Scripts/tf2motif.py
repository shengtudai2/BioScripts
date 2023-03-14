#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author : shengtudai
@Date : 2023-03-11 14:00:00
@Description: This script reads TF information from a file and groups the Motif IDs by TF name, then saves the result to a new file if the second column has content.
@filename : tf2motif.py
"""

import argparse
import pandas as pd


def main(file_path):
    """
    Main function that reads TF information from a file and groups the Motif IDs by TF name, then saves the result to a new file if the second column has content.

    Args:
        file_path (str): Path to the input file containing TF information.

    Returns:
        None
    """
    # Read data from file
    df = pd.read_csv(file_path, sep='\t', index_col=None, header=0)

    # Only keep columns "TF_Name" and "Motif_ID"
    df = df[["DBID", "Motif_ID"]]

    # Only keep rows where DBID starts with "LOC" or "OS"
    df = df[(df["DBID"].str.startswith("LOC")) | (df["DBID"].str.startswith("OS"))]

    # Drop rows with "." in Motif_ID column
    df = df[df["Motif_ID"] != "."]

    df["Motif_ID"] = list(map(lambda x: x.split('_')[0], df["Motif_ID"]))

    # Group Motif IDs by TF name, separated by comma
    df = df.groupby("DBID")["Motif_ID"].apply(lambda x: ",".join(x)).reset_index()

    # Save rows with non-empty Motif_ID to output file
    df = df[df["Motif_ID"].notna()]
    if not df.empty:
        df.to_csv("TF2motif_cisbp.txt", sep="\t", index=False, header=False)


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Group Motif IDs by TF name.")
    parser.add_argument("file_path", type=str, help="Path to the input file containing TF information.")
    args = parser.parse_args()

    # Run main function with parsed arguments
    main(args.file_path)
