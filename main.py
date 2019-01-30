import os
from utils import *

if __name__ == "__main__":
    print("hello world")

    #load_csv_file("data/lapaz_bd_2.csv", ",")
    json_records = load_json_file("data/drugcatalog201901.json")
    csv_data =json_to_csv(json_records)
    save_csv_file(csv_data)

