import pandas as pd
import psutil
log_entries = []

with open("system_logs.txt", "r", encoding="utf-8") as file:
    for line in file:
        # Split by a common separator or parse with regex
        parts = line.strip().split(" ", 3)  # Adjust maxsplit based on your log format
        # print (parts)  # Debugging: print the parts of each log entry
        log_entries.append(parts)
        # Print each log entry for debugging
# Convert into a structured table
df = pd.DataFrame(log_entries, columns=["Datestamp", "Timestamp", "LogLevel", "Message"])
print(df.head())

df.to_csv("structured_logs.csv", index=False)  # Save to CSV for further analysis