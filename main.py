import os
from utils import *

if __name__ == "__main__":
    saving_file_name = "new_dump"
    file_name = "statics/sd-dump.json"
    #csv_data = load_csv_file(file_name, ",")
    #json_data = csv_to_json(csv_data)
    #save_json_file(json_data, saving_file_name)
    #json_records = load_json_file(file_name)
    #csv_data = json_to_csv(json_records)
    #save_csv_file(csv_data, saving_file_name)
    all_data = []
    for i in range(0,2):
        page_url = "https://<>/medicamentos/c/06?q=%3Arelevance&page=" + str(i)
        prize_array = get_html_specific_tag(page_url, "p", "item-prize")
        description_array = get_html_specific_tag(page_url, "p", "item-subtitle")
        text_description_array = get_text_from_object(description_array)
        text_prize_array = get_text_from_object(prize_array)
        data = [{"prize": current_prize, "description": current_description}
                for current_prize, current_description in zip(text_prize_array, text_description_array)]

        all_data = all_data + data

    print(all_data)

