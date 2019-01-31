import csv
import json


def load_json_file(filepath):
    """Obtains the information of a Json dump and stores it as an array of json's"""
    new_json_array = []
    try:
        with open(filepath, 'r') as jsonfile:
            new_json_array = [json.loads(line) for line in jsonfile.readlines()]
    except Exception as e:
        print(e)
    return new_json_array


def load_csv_file(filepath, delimiter=None):
    """Obtains the information of a csv file and stores it on a Matrix ([[0,1,2][0,1,2]])"""
    final_csv_data = []
    try:
        with open(filepath, 'r') as csvfile:
            final_csv_data = [row for row in csv.reader(csvfile, delimiter=delimiter)]
    except Exception as e:
        print(e)
    return final_csv_data


def save_csv_file(csv_data, file_name, delimiter=","):
    """Saves the csv information (a matrix) on a file with csv extension"""
    try:
        with open(file_name + ".csv", "w", newline="") as temp_csv_file:
            temp_file = csv.writer(temp_csv_file, delimiter=delimiter)
            for row in csv_data:
                temp_file.writerow(row)
        return True
    except Exception as e:
        print(e)
        return False


def save_json_file(json_data, file_name):
    """Saves the json data to a file with json extension like a dump"""
    try:
        with open(file_name + ".json", "w") as json_file:
            for jsonrecord in json_data:
                json.dump(jsonrecord, json_file)
        return True
    except Exception as e:
        print(e)
        return False


def json_to_csv(json_records):
    """Converts an array of Json's to a Csv like, Matrix"""
    json_keys = []
    index = 0
    final_csv = []
    try:
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
            final_csv.append(record_row)
            index += 1
    except Exception as e:
        print(e)
    return final_csv


def csv_to_json(csv_data):
    """Converts a Matrix to an Array of Json's"""
    json_records = []
    try:
        json_keys=csv_data[0]
        for csv_row in csv_data[1:]:
            csv_dict = dict()
            index = 0
            for key in json_keys:
                if not csv_row[index]:
                    field = ""
                else:
                    field = csv_row[index]
                csv_dict.update({key: field})
                index += 1

            json_records.append(csv_dict)
    except Exception as e:
        print(e)
    return json_records


    
    
    
    

