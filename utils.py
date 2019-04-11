import csv
import json
import tinys3
import config as conf
import urllib3
from bs4 import BeautifulSoup
import logging
from mongoManager import ManageDB
from itertools import chain

# Load Logging definition
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('tornado-info')


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


def download_upload_image_s3(url, img_name):
    """Download the image from S3 bucket"""
    try:
        http = urllib3.PoolManager()

        response_image = http.request('GET', url, preload_content=False)
        print("status", response_image.status, url)

        with open('images/'+img_name, 'wb') as out:
            while True:
                data = response_image.read(1024)
                if not data:
                    break
                out.write(data)

        conn = tinys3.Connection(conf.AWS_ACCESS_KEY, conf.AWS_SECRET_KEY, tls=True)
        with open("images/"+img_name, 'rb') as myimg:
            conn.upload(conf.FOLDER+img_name, myimg, 'drugs-catalog')

        return True
    except Exception as e:
        logger.error("[ERROR] downloading or uploading images {}".format(e))
        return False


def load_mongo_collection(collection_name=conf.DB_MAIN_COLLECTION):
    """ Return all the records on the collection specified"""
    result = []
    my_db = ManageDB(collection_name)
    try:
        all_records = {}  # All the records without filter
        result = list(my_db.select_json(all_records))  # Convert the cursor to a list

    except Exception as e:
        logger.info("[ERROR] loading the mongo collection: {}".format(e))
    finally:
        if my_db is not None:
            my_db.close()

    return result


def modify_collection_fields(data_json_list, keys_list, collection_name=conf.DB_MAIN_COLLECTION):
    """Update the entire collection with a json array taking as id the specified id_key"""
    result = []
    my_db = ManageDB(collection_name)
    try:

        for data_json in data_json_list:
            json_keys = dict()
            for key in keys_list:
                # Get all the keys and assign the value valid for the current data json (document)
                json_keys.update({key: data_json.get(key)})
            result = my_db.update(json_keys, data_json)

        result = data_json_list
    except Exception as e:
        logger.info("[ERROR] updating the mongo fields: {}".format(e))
    finally:
        if my_db is not None:
            my_db.close()

    return result


def get_html_page(page_url):
    """ Get the whole page source code"""
    http = urllib3.PoolManager()
    response = http.request('GET', page_url)
    soup = BeautifulSoup(response.data, 'html.parser')
    response.release_conn()
    return soup


def get_soup_obj_by_dom_tag(soup, object_dom, tag_value, object_tag="class"):
    """ Search for all the objects in the current soup object with this specific HTML dom and tag value"""
    object_array = soup.find_all(object_dom, attrs={object_tag: tag_value})
    return object_array


def get_soup_obj_by_dom(soup, object_dom):
    """ Search for all the objects in the current soup object with this specific HTML dom and tag value"""
    object_array = soup.find_all(object_dom)
    return object_array


def get_soup_tables_on_single_table(soup, table_tag_value, table_tag="class", columns_to_keep=[]):
    """ Search for all the objects in the current soup object with this specific HTML dom and tag value"""
    new_table_array = []
    tables_array = soup.find_all("table", attrs={table_tag: table_tag_value})
    for current_table in tables_array:
        table_body = current_table.find('tbody')
        table_rows = table_body.find_all('tr')
        table_rows.pop(0)  # Remove the column names
        table_rows.pop(-1)  # Remove the last column names
        for row in table_rows:
            if not columns_to_keep:
                new_table_array.append(row)
            else:
                new_row = []
                table_fields = row.find_all('td')
                for index in columns_to_keep:
                    if table_fields[index]:
                        new_row.append(table_fields[index])
                new_table_array.append(new_row)

    return new_table_array


def get_html_obj_by_dom_tag(page_url, object_dom, tag_value, object_tag="class"):
    """ Search for all the objects in the current url with this specific HTML dom and class"""
    http = urllib3.PoolManager()
    response = http.request('GET', page_url)
    soup = BeautifulSoup(response.data, 'html.parser')

    object_array = soup.find_all(object_dom, attrs={object_tag: tag_value})
    response.release_conn()
    return object_array


def get_text_from_object(object_array):
    """ Receives a soup4 object array and returns a string array with the text of each object"""
    return [current_tag.text.strip() for current_tag in object_array]


def get_tag_from_object(object_array, tag):
    """ Receives a soup4 object array and returns a string array with the text of the tag of each object"""
    return [current_tag.get(tag) for current_tag in object_array]


def search_by_key_json(key_json, collection_name=conf.DB_MAIN_COLLECTION):
    """ Search on the db by the received json keys object"""
    my_db = ManageDB(collection_name)
    result = []
    try:
        result = my_db.select_json(key_json)

    except Exception as e:
        logger.info("[ERROR] searching documents by json {}".format(e))
    finally:
        if my_db is not None:
            my_db.close()

    return result
