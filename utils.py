import os
import csv
import json

LINE_END = "\n"
def load_json_file(filepath):
    new_json_array = None
    try:
        with open(filepath, 'r') as jsonfile:
            new_json_array = [json.loads(line) for line in jsonfile.readlines()]
    except Exception as e:
        print(e)
    return new_json_array


def load_csv_file(filepath, delimiter=None):
    final_csv_data = []
    try:
        with open(filepath, 'r') as csvfile:
            final_csv_data =[row for row in csv.reader(csvfile, delimiter=delimiter)]
        return final_csv_data
    except Exception as e:
        print(e)
        return False


def save_csv_file(csv_data, delimiter=","):
    print("csv data")
    with open("new_csv_file.csv", "w") as temp_csv_file:
        csv.writer(temp_csv_file, delimiter=delimiter)

    return True


def save_json_file(json_data):
    print("json data")

def json_to_csv(json_records):
    print("json to csv")
    json_keys = []
    index = 0
    final_csv = []
    for record in json_records:
        record_row = []
        for key, value in record.items():
            if key == "_id":
                continue
            if index == 0:
                json_keys.append(key)
            record_row.append(value)
        if index == 0:
            final_csv.append(json_keys)
            print(final_csv)
        final_csv.append(record_row)
        index += 1

    return final_csv

