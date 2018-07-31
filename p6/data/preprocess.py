#!/usr/bin/python
"""Downloads and aggregates data files using multiprocessing
The target data files are stored in csv format and compressed using bzip2. Multithreading is used
to download multiple files concurrently. After the files are downloaded aggregation data is calculated
concurrently using multiprocessing.
"""
import concurrent.futures
import requests
import os
import pandas as pd
import pickle

URLS = [f'http://stat-computing.org/dataexpo/2009/{year}.csv.bz2'
        for year in range(1987, 2009)]

# Define features to load when reading the CSVs into pandas
FEATURES_OF_INTEREST = [
    'Year',
    'UniqueCarrier',
    'DepDelay'
]

# Features to group by
GROUP_BY = ['Year', 'UniqueCarrier']

# Mapping of aggregation functions to features
AGG_MAP = {
    'DepDelay': lambda x: (x>15).sum()/len(x)
}

with open('carrier_dict.pkl', 'rb') as file:
    CARRIER_MAP = pickle.load(file)


def load_url(url, process_executor):
    """Downloads URL if the file does not already exist

    Passes filename to aggregation function via a process executor for conccurent aggregation.
    Returns a reference to the future object created by the process executor
    """
    filename = url.split('/')[-1]
    if not os.path.exists(filename):
        print(f'Downloading {url}')
        r = requests.get(url)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
        print(f'Downloaded {url}. Passing to aggregator.')
    else:
        print(f'{filename} already exists. Passing to aggregator.')
    return process_executor.submit(aggregate_data, filename)


def aggregate_data(filename):
    """Aggregate data from raw file

    The files are stored in bz2 format. Pandas is used to decompress the file, extract
    FEATURES_OF_INTEREST and calculate aggregated information.
    """
    print(f'Processing {filename}')
    # Unzip and read the csv
    df = pd.read_csv(filename, usecols=FEATURES_OF_INTEREST, compression='bz2')
    # Convert the carrier codes to their full names
    df['UniqueCarrier'] = df['UniqueCarrier'].map(CARRIER_MAP)
    # Aggregate and reduce the dataframe
    df = df.groupby(GROUP_BY).agg(AGG_MAP)
#    df.set_index(GROUP_BY, inplace=True)
    print(f'Processed: {filename}')
    return df


if __name__ == '__main__':
    # Verify feature mapping variables are correct before beginning
    for feature in GROUP_BY:
        assert feature in FEATURES_OF_INTEREST, f'Unexpected feature {feature} in group_by.'
    for feature in AGG_MAP.keys():
        assert feature in FEATURES_OF_INTEREST, f'Unexpected feature {feature} in aggregation map.'

    with concurrent.futures.ProcessPoolExecutor() as pe, concurrent.futures.ThreadPoolExecutor() as te:
        future_url_request = [te.submit(load_url, url, pe) for url in URLS]

        processes = []
        for future in concurrent.futures.as_completed(future_url_request):
            processes.append(future.result())

        aggregated_data = []
        for future in concurrent.futures.as_completed(processes):
            aggregated_data.append(future.result())

    results = pd.concat(aggregated_data)
    # Resetting the index converts the result to tidy data format
    results.reset_index(inplace=True)
    results.to_csv('flight_data.csv')
