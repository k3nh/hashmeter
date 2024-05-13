# hashmeter
monitor system for capacity purposes based on utilizaiton

Got it! Here's the updated `README.md` that reflects the use of `uv` instead of `pip` for installing dependencies:

```markdown
# Hashmeter

## Overview

Hashmeter is a tool that performs PBKDF2 hashing to sample CPU load periodically. It measures the time taken to compute the hash and uses a T-Digest to maintain and export timing statistics. The tool continuously hashes, records timing statistics, and periodically prints out various percentiles of the timing data.

## Intent

- **Measure CPU Load:** By performing a known computationally intensive task (PBKDF2 hashing) regularly.
- **Timing Statistics:** Capture and analyze how long it takes to perform the hashing by maintaining a T-Digest.
- **Periodical Updates:** Print out the timing statistics every 15 seconds and export the T-Digest to a JSON file.

## Prerequisites

- Python 3.6+
- Unix-based OS (Linux, macOS)

## Setup

To set up the environment and install the required libraries, run the `setup.sh` script.

### `setup.sh`

```sh
#!/bin/bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Update pip (optional but recommended)
pip install --upgrade pip

# Install required libraries using uv
uv pip install tdigest
uv pip install asyncio
uv pip install uvloop

# Deactivate the virtual environment
deactivate
```

## Usage

1. **Setup the virtual environment and install dependencies:**

    ```sh
    bash setup.sh
    ```

2. **Activate the virtual environment:**

    ```sh
    source .venv/bin/activate
    ```

3. **Run the script:**

    ```sh
    python hashmeter.py
    ```

4. **View the Output:**

    The script prints the following metrics every 15 seconds:
    - `Current`: The time taken (in microseconds) for the most recent PBKDF2 hashing.
    - `Count`: The number of timing samples collected.
    - `Min`: The minimum time taken.
    - `25th`: The 25th percentile time taken.
    - `50th`: The median (50th percentile) time taken.
    - `75th`: The 75th percentile time taken.
    - `95th`: The 95th percentile time taken.
    - `99th`: The 99th percentile time taken.
    - `Max`: The maximum time taken.
```% python hashmeter.py

Current  Count    Min      25th     50th     75th     95th     99th     Max     
262 μs   484      254 μs   794 μs   1365 μs  1599 μs  8989 μs  8989 μs  8989 μs 
1503 μs  485      254 μs   795 μs   1363 μs  1597 μs  8989 μs  8989 μs  8989 μs 
1454 μs  486      254 μs   797 μs   1364 μs  1599 μs  8989 μs  8989 μs  8989 μs 
1349 μs  487      254 μs   799 μs   1364 μs  1602 μs  8989 μs  8989 μs  8989 μs 
742 μs   488      254 μs   797 μs   1364 μs  1604 μs  8989 μs  8989 μs  8989 μs 
1449 μs  489      254 μs   799 μs   1365 μs  1605 μs  8989 μs  8989 μs  8989 μs 
1399 μs  490      254 μs   801 μs   1366 μs  1604 μs  8989 μs  8989 μs  8989 μs 
1345 μs  491      254 μs   803 μs   1366 μs  1604 μs  8989 μs  8989 μs  8989 μs 
821 μs   492      254 μs   805 μs   1366 μs  1605 μs  8989 μs  8989 μs  8989 μs 
664 μs   493      254 μs   799 μs   1365 μs  1605 μs  8989 μs  8989 μs  8989 μs 
699 μs   494      254 μs   797 μs   1365 μs  1605 μs  8989 μs  8989 μs  8989 μs
```

5. **Deactivate the virtual environment after use:**

    ```sh
    deactivate
    ```

## Files

- **`hashmeter.py`**: The main script that performs the hashing, measures timing, and manages the T-Digest.
- **`setup.sh`**: Script to set up the virtual environment and install necessary libraries.
- **`hashmeter.json`**: (Automatically created) JSON file used to save timing statistics via T-Digest.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
