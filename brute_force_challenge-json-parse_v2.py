# brute_force_challenge-json-parse_v2.py

# The Challenge:
# Each entry in json/attempts.json has the format <<---- ##### Because this is how the REAL-World works; parsing logs/files! #####
# {"ip_address": "203.0.113.5", "seconds_offset": 40}
# Return IPs with MORE THAN 3 access attempts within any 60-second window.

import json
import sys
from pathlib import Path

# Step 1: Load the attempts from the external JSON file.
# Path(__file__).parent is the folder this script is in, so the file is
# found no matter which folder you run the script from.
# json.load() turns the file into a Python list of dictionaries.
# try/except: if the file is missing or broken, stop with a clear message.

attempts_file_path = Path(__file__).parent / "json" / "attempts.json"

try:
    with open(attempts_file_path, encoding="utf-8") as attempts_file:
        attempts = json.load(attempts_file)
except FileNotFoundError:
    sys.exit(f"Error: could not find the file {attempts_file_path}")
except json.JSONDecodeError as json_error:
    sys.exit(f"Error: {attempts_file_path} is not valid JSON ({json_error})")

if not isinstance(attempts, list):
    sys.exit("Error: the JSON file must contain a list [ ... ] of IPs and seconds")

# Step 2: Set the limits.
# More than 3 attempts (4 or more) within 60 seconds is suspicious.

MAX_ALLOWED_ATTEMPTS = 3
TIME_FRAME_SECONDS = 60

# Step 3: Group the attempt times by IP.
# Each attempt_record is one dictionary from the JSON file.
# Bad entry? Print which one and why, then skip it (continue).
# New IP? Start it with an empty list. Then add the time to its list.
# Example result: {"203.0.113.5": [40, 0, 20, 55], ...}

offsets_by_ip = {}

for record_number, attempt_record in enumerate(attempts, start=1):
    if not isinstance(attempt_record, dict):
        print(f"Skipping entry {record_number}: it is not a {{ ... }} object")
        continue
    if "ip_address" not in attempt_record or "seconds_offset" not in attempt_record:
        print(f"Skipping entry {record_number}: missing ip_address or seconds_offset")
        continue

    ip_address_key = attempt_record["ip_address"]
    seconds_offset_value = attempt_record["seconds_offset"]

    if not isinstance(ip_address_key, str):
        print(f"Skipping entry {record_number}: ip_address must be text")
        continue
    if not isinstance(seconds_offset_value, int):
        print(f"Skipping entry {record_number}: seconds_offset must be a whole number")
        continue
    # Rule: seconds_offset must be >= 0. Zero is valid; only negatives are skipped.
    if seconds_offset_value < 0:
        print(f"Skipping entry {record_number}: seconds_offset cannot be negative")
        continue
    
    if ip_address_key not in offsets_by_ip:
        offsets_by_ip[ip_address_key] = []
    offsets_by_ip[ip_address_key].append(seconds_offset_value)

# Step 4: Find IPs with more than 3 attempts within 60 seconds.
# Sort each IP's times. Start a 60-second time frame at each attempt.
# attempt_count: adds 1 for each attempt inside that time frame.
# highest_attempt_count: the biggest attempt_count found for this IP.
# More than 3? Save the IP and its highest_attempt_count.

highest_attempt_count_by_ip = {}  # key = IP address, value = its highest_attempt_count

for suspicious_ip_address_key, offsets_value in offsets_by_ip.items():
    offsets_value.sort()
    highest_attempt_count = 0
    for first_attempt_index in range(len(offsets_value)):
        time_frame_end_time = offsets_value[first_attempt_index] + TIME_FRAME_SECONDS
        attempt_count = 0
        for seconds_offset_value in offsets_value[first_attempt_index:]:
            if seconds_offset_value < time_frame_end_time:
                attempt_count += 1
        if attempt_count > highest_attempt_count:
            highest_attempt_count = attempt_count
    if highest_attempt_count > MAX_ALLOWED_ATTEMPTS:
        highest_attempt_count_by_ip[suspicious_ip_address_key] = highest_attempt_count

# Step 5: Print a heading.
print("\nSuspicious ⚠ IPs:")
print("-----------------")

# Step 6: Sort the IPs lowest first, then print each with its time frame count.
# sorted() on a dictionary gives back its keys (the IPs) in order.
# Expected: 172.16.5.20 - 4 attempts, 203.0.113.5 - 4 attempts
for suspicious_ip_address_key in sorted(highest_attempt_count_by_ip):
    print(f"IPv4 Address: \033[1;31m{suspicious_ip_address_key}\033[0m | 🔥 \033[1;33m{highest_attempt_count_by_ip[suspicious_ip_address_key]}" \
          + f"\033[0m attempts within 🚨 {TIME_FRAME_SECONDS} seconds")

