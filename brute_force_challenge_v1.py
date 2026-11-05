# brute_force_challenge_v1.py

# The Challenge:
# Each entry in 'attempts' has format (ip_address, seconds_offset)
# Return IPs with MORE THAN 3 access attempts within any 60-second window.

attempts = [
    ("203.0.113.5", 40),
    ("198.51.100.9", 140),
    ("192.0.2.44", 25),
    ("172.16.5.20", 100),
    ("203.0.113.99", 10),
    ("203.0.113.5", 0),
    ("172.16.5.20", 0),
    ("198.51.100.9", 0),
    ("192.0.2.44", 0),
    ("203.0.113.99", 0),
    ("172.16.5.20", 135),
    ("198.51.100.9", 70),
    ("203.0.113.5", 20),
    ("192.0.2.44", 200),
    ("203.0.113.99", 20),
    ("172.16.5.20", 115),
    ("203.0.113.5", 55),
    ("198.51.100.9", 210),
    ("192.0.2.44", 50),
    ("172.16.5.20", 150),
]

# Step 1: Set the limits.
# More than 3 attempts (4 or more) within 60 seconds is suspicious.
MAX_ALLOWED_ATTEMPTS = 3
TIME_FRAME_SECONDS = 60

# Step 2: Group the attempt times by IP.
# New IP? Start it with an empty list. Then add the time to its list.
# Example result: {"203.0.113.5": [40, 0, 20, 55], ...}

offsets_by_ip = {}

for ip_address_key, seconds_offset_value in attempts:
    if ip_address_key not in offsets_by_ip:
        offsets_by_ip[ip_address_key] = []
    offsets_by_ip[ip_address_key].append(seconds_offset_value)

# Step 3: Find IPs with more than 3 attempts within 60 seconds.
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

# Step 4: Print a heading.
print("\nSuspicious ⚠ IPs:")
print("-----------------")

# Step 5: Sort the IPs lowest first, then print each with its time frame count.
# sorted() on a dictionary gives back its keys (the IPs) in order.
# Expected: 172.16.5.20 - 4 attempts, 203.0.113.5 - 4 attempts
for suspicious_ip_address_key in sorted(highest_attempt_count_by_ip):
    print(f"IPv4 Address: \033[1;31m{suspicious_ip_address_key}\033[0m | 🔥 \033[1;33m{highest_attempt_count_by_ip[suspicious_ip_address_key]}" \
          + f"\033[0m attempts within 🚨 {TIME_FRAME_SECONDS} seconds")
