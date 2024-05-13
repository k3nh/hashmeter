# hashtimer.py
# k.hunt Starficient

import uvloop
import asyncio
import hashlib
import hmac
import time
from tdigest import TDigest
import json
import os

async def pbkdf2_hash(password, salt, iterations, key_size):
    """
    Perform PBKDF2 hashing and measure the execution time using a monotonic clock.

    Args:
        password (bytes): The password to be hashed.
        salt (bytes): The salt used in the hashing process.
        iterations (int): The number of iterations for PBKDF2.
        key_size (int): The size of the derived key.

    Returns:
        tuple: A tuple containing the hashed password and the execution time in microseconds.
    """
    start_time = time.monotonic()  # Get the start time using a monotonic clock
    hashed_password = hashlib.pbkdf2_hmac('sha256', password, salt, iterations, key_size)
    end_time = time.monotonic()  # Get the end time using a monotonic clock
    timing_value = (end_time - start_time) * 1e6  # Calculate the timing value in microseconds
    return hashed_password, timing_value

def export_tdigest(td, filename):
    """
    Export the T-Digest data to a JSON file.

    Args:
        td (TDigest): The T-Digest object to be exported.
        filename (str): The name of the JSON file to export the data to.
    """
    centroids = td.centroids_to_list()
    data = {'centroids': centroids}
    with open(filename, 'w') as file:
        json.dump(data, file)

def import_tdigest(filename):
    """
    Import the T-Digest data from a JSON file.

    Args:
        filename (str): The name of the JSON file to import the data from.

    Returns:
        TDigest: The imported T-Digest object, or a new empty T-Digest if the file doesn't exist.
    """
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            centroids = data['centroids']
            td = TDigest()
            td.update_centroids_from_list(centroids)
            return td
    else:
        return TDigest()
def interpolate(td, q):
    """
    Interpolate the quantile value from the T-Digest.

    Args:
        td (TDigest): The T-Digest object.
        q (float): The quantile to estimate (0 <= q <= 1).

    Returns:
        float: The estimated quantile value.
    """
    centroids = td.centroids_to_list()
    n = td.n
    q_min = 0.0
    q_max = 1.0
    
    for i, c in enumerate(centroids):
        q_left = q_min + (c['c'] - 1) / (2 * n)
        q_right = q_min + (c['c'] + 1) / (2 * n)
        
        if q < q_right:
            if i == 0:
                return round(c['m'])  # First centroid, return its mean rounded to nearest integer
            elif c['c'] == 1:
                delta_q = (q - q_left) / (q_right - q_left)
                return round(centroids[i-1]['m'] + delta_q * (c['m'] - centroids[i-1]['m']))
            else:
                delta_q = (q - q_left) / (q_right - q_left)
                return round(c['m'] - (c['m'] - centroids[i-1]['m']) / 2 + delta_q * (c['m'] - centroids[i-1]['m']))
        
        q_min = q_right
    
    return round(centroids[-1]['m'])  # Last centroid, return its mean rounded to nearest integer


async def main():
    """Main function to perform PBKDF2 hashing, measure timing, and manage T-Digest.

    This function continuously performs PBKDF2 hashing, measures execution time,
    updates T-Digest with timing values, and exports T-Digest data to a JSON file.
    It also imports T-Digest data from the JSON file on startup if it exists.
    The function displays T-Digest statistics every 15 seconds.
    """
    password = b"mysecretpassword"
    salt = b"somesalt"
    iterations = 1000
    key_size = 32
    tdigest_filename = 'hashmeter.json'

    td = import_tdigest(tdigest_filename)

    # Dynamic compression factor based on the number of samples
    if td.n < 1000:
        delta = 50
    elif td.n < 10000:
        delta = 100
    else:
        delta = 200

    print("{:<8} {:<8} {:<8} {:<8} {:<8} {:<8} {:<8} {:<8} {:<8}".format(
        "Current", "Count", "Min", "25th", "50th", "75th", "95th", "99th", "Max"
    ))

    while True:
        hashed_password, timing_value = await pbkdf2_hash(password, salt, iterations, key_size)
        td.update(timing_value)  # Store the timing value in the T-Digest

        percentiles = [interpolate(td, p / 100) for p in [25, 50, 75, 95, 99]]

        print("{:<8} {:<8} {:<8} {:<8} {:<8} {:<8} {:<8} {:<8} {:<8}".format(
            "{} μs".format(round(timing_value)),
            int(td.n),
            "{} μs".format(interpolate(td, 0.0)),
            "{} μs".format(percentiles[0]),
            "{} μs".format(percentiles[1]),
            "{} μs".format(percentiles[2]),
            "{} μs".format(percentiles[3]),
            "{} μs".format(percentiles[4]),
            "{} μs".format(interpolate(td, 1.0))
        ))

        export_tdigest(td, tdigest_filename)

        await asyncio.sleep(15)  # Wait for 15 seconds

if __name__ == "__main__":
    uvloop.install()
    asyncio.run(main())

if __name__ == "__main__":
    uvloop.install()
    asyncio.run(main())
