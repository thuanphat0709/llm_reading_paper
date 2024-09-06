import os
import ingest_full
import makechain_full
import make_chain_supersum
from concurrent.futures import ThreadPoolExecutor
from threading import current_thread
import logging
from datetime import datetime
import constants
import json
import csv
from pathlib import Path
import time

# PLEASE "cd app" BEFORE RUNNING!

source_dir = "docs"

def run(writer, f, writer1, f1, file_path):
    try:
        document = ingest_full.ingest_run(file_path)
        response = makechain_full.make_chain(document)
        result = json.loads(response)
        result1 = json.loads(make_chain_supersum.make_chain(response))
        row = [
            result["Title"],
            result["Authors"],
            result["Issued year"],
            result["Research subject / Main focus"],
            result["Key words"],
            result["Hypothesis"],
            result["Key finding"],
            result["Implication"],
            result["Trading strategy"],
            result["Sample period"],
            result["Sample market"],
            result["Sample size"],
            result["Backest results"],
            result["Risk management"]
        ]

        row1 = [
            result1["Title"],
            result1["Authors"],
            result1["Issued year"],
            result1["Hypothesis"],
            result1["Trading strategy"],
            result1["Testing period"],
            result1["Finding"],
            result1["Quantitative Results"]
        ]

        writer.writerow(row)
        f.flush()
        writer1.writerow(row1)
        f1.flush()

        # Check if the file exists, then delete it
        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        print(f"Error occurred with file: {file_path}")
        print(f"Exception: {e}")
        print('')

# Get all filepaths of pdf file in the docs folder
filepaths_list = os.listdir(source_dir)

def output():
    current_time = datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
    csv_file_sum = f"data/sum{current_time}.csv"
    csv_file_supersum = f"data/supersum{current_time}.csv"

    with open(csv_file_sum, 'w', newline='') as f1, open(csv_file_supersum, 'w', newline='') as f2:
        writer1 = csv.writer(f1)
        writer2 = csv.writer(f2)
        header1 = [
                "Title",
                "Authors",
                "Issued year",
                "Research subject / Main focus",
                "Key words",
                "Hypothesis",
                "Key finding",
                "Implication",
                "Trading strategy",
                "Sample period",
                "Sample market",
                "Sample size",
                "Backest results",
                "Risk management"
        ]
        header2 = [
            "Title",
            "Authors",
            "Issued year",
            "Hypothesis",
            "Trading strategy",
            "Testing period",
            "Finding",
            "Quantitative Results"
        ]

        writer1.writerow(header1)
        writer2.writerow(header2)
        
        with ThreadPoolExecutor(max_workers = min(len(filepaths_list), 5)) as executor:  
            _ = executor.map(lambda sim: run(writer1, f1, writer2, f2, sim), filepaths_list)
try:
    output()
except Exception as e:
    print(f'Issue occurred! {type(e).__name__}: {e}')
    