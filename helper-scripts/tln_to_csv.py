#!/usr/bin/env python3
import csv
import sys
from datetime import datetime, timezone

def parse_tln_line(line):
    """
    TLN format:
    time|source|host|user|description
    """
    parts = line.rstrip("\n").split("|", 4)

    if len(parts) != 5:
        return None

    epoch, source, host, user, description = parts

    # Convert epoch → YYYY-MM-DD HH:MM:SS (UTC)
    try:
        epoch_int = int(epoch)
        human_time = datetime.fromtimestamp(epoch_int, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        human_time = "INVALID_TIMESTAMP"

    return {
        "Time": human_time,
        "Source": source,
        "Host": host,
        "User": user,
        "Description": description
    }

def convert_tln_to_csv(tln_path, csv_path):
    with open(tln_path, "r", encoding="utf-8") as infile, \
         open(csv_path, "w", newline="", encoding="utf-8") as outfile:

        writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)

        # Header row
        writer.writerow(["Time", "Source", "Host", "User", "Description"])

        for line in infile:
            if not line.strip():
                continue

            parsed = parse_tln_line(line)
            if parsed is None:
                sys.stderr.write(f"Skipping malformed TLN line: {line}")
                continue

            # Force Description to be quoted
            writer.writerow([
                parsed["Time"],
                parsed["Source"],
                parsed["Host"],
                parsed["User"],
                f"{parsed['Description']}"
            ])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: tln_to_csv.py input.tln output.csv")
        sys.exit(1)

    convert_tln_to_csv(sys.argv[1], sys.argv[2])
