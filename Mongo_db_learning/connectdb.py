'''--------------------------------------------->
THIS WILL HELP IN SENDING YOUR DICTIONARY TO THE MONGODB
---------------------------------------------------->'''

import pymongo
import pandas as pd 
import os

connection_string = "mongodb://localhost:27017/weather"
client = pymongo.MongoClient(connection_string)
db = client.get_database()
db["forcast_collection"].drop()
db.create_collection("forcast_collection")


collection = db['forcast_collection']

data = [
    {"name": "John", "age": 30, "city": "New York"},
    {"name": "Jane", "age": 25, "city": "San Francisco"},
    {"name": "Bob", "age": 35, "city": "Los Angeles"}
]

result =collection.insert_many(data)
result.inserted_ids


all_data = collection.find()
data_list=list(all_data)

import  csv
csv_file_name ='data.csv'
with open('csv_file_name',"w",newline='') as csv_file:
  fieldnames = data_list[0].keys()
  writer = csv.DictWriter(csv_file,fieldnames = fieldnames)
  writer.writeheader()
  writer.writerows(data_list)