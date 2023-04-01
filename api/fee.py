import datetime
import math

# Take input for time in and time out in HH:MM:SS format
time_in_str = input("Enter the time in (in format 'HH:MM:SS'): ")
time_out_str = input("Enter the time out (in format 'HH:MM:SS'): ")

# Convert input strings to datetime.time objects
time_in = datetime.datetime.strptime(time_in_str, '%H:%M:%S').time()
time_out = datetime.datetime.strptime(time_out_str, '%H:%M:%S').time()

# Calculate time difference in hours
time_diff = (datetime.datetime.combine(datetime.date.today(), time_out) - datetime.datetime.combine(datetime.date.today(), time_in)).total_seconds() / 3600

# Check if time difference is less than or equal to 0.25 (15 minutes)
if time_diff <= 0.25:
    fee = 0
elif time_diff > 0.25 and time_diff < 1:
    fee = 20
else:
    # Calculate fee based on policy of 20 baht per hour
    fee = math.ceil(time_diff) * 20

# Print fee
print(f"The fee is {fee:.2f} baht")