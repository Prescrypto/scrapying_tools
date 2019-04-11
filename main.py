import os
from utils import *
from decimal import Decimal
from re import sub

if __name__ == "__main__":
    saving_file_name = "statics/temp_dump"
    file_name = "statics/sd-dump.json"
    #csv_data = load_csv_file(file_name, ",")
    #json_data = csv_to_json(csv_data)
    #save_json_file(json_data, saving_file_name)
    #json_records = load_json_file(file_name)
    #csv_data = json_to_csv(json_records)
    #save_csv_file(csv_data, saving_file_name)
    all_data = []
    #for i in range(0, 164):
    db_list = load_mongo_collection()
    for db_doc in db_list:
        if db_doc.get("upc") != "" and db_doc.get("upc") != "0":
            page_url = "https://<>/search/?text={}".format(db_doc.get("upc"))
            soup = get_html_page(page_url)
            image_array = get_soup_specific_tag(soup, "img", "item-image img-responsive")
            image_srcs = get_tag_from_object(image_array, "src")
            if len(image_srcs) > 0:
                img_url = image_srcs[0]
                if "https://s3-us-west-2" not in db_doc.get("image_url", "").split("."):
                    image_uploaded = download_upload_image_s3(img_url, db_doc.get("upc"))
                    if image_uploaded:
                        s3_img_url = conf.S3_BASE_URL.format(db_doc.get("upc"))
                        data = {"upc": db_doc.get("upc"), "image_url": s3_img_url}
                        all_data.append(data)
    json_keys = ["upc"]

    result = modify_collection_fields(all_data, json_keys, conf.DB_MAIN_COLLECTION)
