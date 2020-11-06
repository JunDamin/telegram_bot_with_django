import csv

def write_csv(record, header: list, file_name: str):
    with open(file_name, mode="w", encoding="utf-8-sig") as signing_file:
        writer = csv.writer(signing_file)
        writer.writerow(header)
        writer.writerows(record)
