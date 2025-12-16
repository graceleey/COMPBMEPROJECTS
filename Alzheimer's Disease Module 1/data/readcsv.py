import csv

with open("UpdatedMetaData.csv", newline ="") as f:
    reader = csv.reader(f)
    headers = next(reader)
    for h in headers: print(h)
    