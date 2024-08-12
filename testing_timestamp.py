import datetime

# Unix timestamp in milliseconds
timestamp =1581536080691
# Convert to seconds
timestamp_seconds = timestamp / 1000.0

# Convert to datetime object
date_time = datetime.datetime.fromtimestamp(timestamp_seconds)

# Print the readable date and time
print(date_time.strftime('%Y-%m-%d %H:%M:%S'))
