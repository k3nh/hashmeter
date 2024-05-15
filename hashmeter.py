import uvloop
import asyncio
import hashlib
import hmac
import time
from tdigest import TDigest
import json
import os

async def pbkdf2_hash(password, salt, iterations, key_size):
    start_time = time.monotonic()
    hashed_password = hashlib.pbkdf2_hmac('sha256', password, salt, iterations, key_size)
    end_time = time.monotonic()
    timing_value = (end_time - start_time) * 1e6
    return hashed_password, timing_value

def export_tdigest(td, filename):
    centroids = td.centroids_to_list()
    data = {'centroids': centroids}
    with open(filename, 'w') as file:
        json.dump(data, file)

def import_tdigest(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        centroids = data['centroids']
        td = TDigest()
        td.update_centroids_from_list(centroids)
        return td
    else:
        return TDigest()

def log_timing_value(timing_value, log_filename):
    current_time = int(time.time())
    with open(log_filename, 'a') as log_file:
        log_file.write(f"{current_time},{timing_value}\n")

async def main():
    password = b"mysecretpassword"
    salt = b"somesalt"
    iterations = 1000
    key_size = 32

    tdigest_filename = 'hashmeter.json'
    log_filename = 'timing_values.log'

    td = import_tdigest(tdigest_filename)

    if td.n < 1000:
        delta = 50
    elif td.n < 10000:
        delta = 100
    else:
        delta = 200

    print("{:<10} {:<8} {:<8} {:<8} {:<8} {:<8} {:<8} {:<8} {:<8}".format(
        "Current", "Count", "Min", "25th", "50th", "75th", "95th", "99th", "Max"
    ))

    while True:
        hashed_password, timing_value = await pbkdf2_hash(password, salt, iterations, key_size)
        td.update(timing_value)
        log_timing_value(timing_value, log_filename)

        percentiles = [td.percentile(p) for p in [25, 50, 75, 95, 99]]

        print("{:<10} {:<8} {:<8} {:<8} {:<8} {:<8} {:<8} {:<8} {:<8}".format(
            f"{int(timing_value)} μs",
            int(td.n),
            f"{int(td.percentile(0))} μs",
            f"{int(percentiles[0])} μs",
            f"{int(percentiles[1])} μs",
            f"{int(percentiles[2])} μs",
            f"{int(percentiles[3])} μs",
            f"{int(percentiles[4])} μs",
            f"{int(td.percentile(100))} μs"
        ))

        export_tdigest(td, tdigest_filename)
        await asyncio.sleep(15)

if __name__ == "__main__":
    uvloop.install()
    asyncio.run(main())
