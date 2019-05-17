# scraping_tools
Scraping Tools

This is a serie of basic tools for json and csv files
to convert, read and save this kind of formats

To get started you have to execute the requirements.txt file:

```pip install -r requirements.txt```

Then in the main namespace you can call the methods you need, to scrape the page, as example you can use the following script to obtain the title, image and description of a products catalog on a certain page and then store the data on mongodb:

First we need to initialize the Environment variables to our own.
For this example we need to set:
```
DB_MAIN_COLLECTION = The name of the collection we are going to get and update (if we want to insert the new information to another collection we just have to send that field when calling the 
load_mongo_collection(collection_name=<NEW NAME>)
or the
modify_collection_fields(data_json_list, keys_list, collection_name=<NEW NAME>)```

AWS_ACCESS_KEY = Amazon access key
AWS_SECRET_KEY = Amazon secret key
FOLDER = S3 Folder
S3_BASE_URL = "https://s3-us-west-2.amazonaws.com/<BUCKET NAME>/<S3 FOLDER>/{}.png"
MONGO_URI = Yo can change the uri to your own, local or remote
DEFAULT_DB = The data base name
```

``` 
import os
from utils import *
from decimal import Decimal
from re import sub

if __name__ == "__main__":
    all_data = []
    # First we load a complete collection (table) from mongo 
    # with our products bar code so we can use it on the search
    db_documents_array = load_mongo_collection()
    # Now product by product we get the upc (bar code) and add it to the search url as a param,
    # in this case, the param needed is "text"
    for db_doc in db_documents_array:
        if db_doc.get("upc") != "" and db_doc.get("upc") != "0":
            page_url = "https://<URL OF THE PAGE TO SCRAPE>/search/?text={}".format(db_doc.get("upc"))
            # Now the get_html_page method performs a GET request to the url and obtains all of it's code
            # then it stores the code as a Soup object and closes the conection so we don't have to
            # make another request to the same page.
            soup = get_html_page(page_url)
            # The get_soup_obj_by_dom_tag method takes the entire soup object and search for a object which has
            # a specific Dom and class tags in this case, we're searching by
            # Dom =  "img"  Class Tags =  "item-image img-responsive"
            image_array = get_soup_obj_by_dom_tag(soup, "img", "item-image img-responsive")
            # Now what we really want from this object (an image) is it's source/url 
            # To get it the get_tag_from_object method receives the specific soup object array and the tag
            # we are searching for, in this case "src"
            image_srcs = get_tag_from_object(image_array, "src")
            # Now to work with the sources first we check if the resulting array has any
            # And then as we only care the first one in the array, we call the download_upload_image_s3 method
            # which will download the image from the source and then upload it to our own S3 bucket naming it 
            # with the bar code we already had on the data base
            if len(image_srcs) > 0:
                img_url = image_srcs[0]
                image_uploaded = download_upload_image_s3(img_url, db_doc.get("upc"))
                # Then if the image was successfully uploaded we are updating the collection array with
                # it's new s3 image url
                if image_uploaded:
                    s3_img_url = conf.S3_BASE_URL.format(db_doc.get("upc"))
                    data = {"upc": db_doc.get("upc"), "image_url": s3_img_url}
                    all_data.append(data)
    # And finally we set the upc (bar code) as the key for each document (json) in the collection array
    # so the changes can be updated in the data base
    json_keys = ["upc"]
    result = modify_collection_fields(all_data, json_keys, conf.DB_MAIN_COLLECTION)


```
