from pymongo import MongoClient
import pyarrow.parquet as pq
import gdown
import os
import pandas as pd

# Downloading of parquet data from Google Drive link using gdown
file_path = os.path.dirname(os.path.realpath(
    __file__)) + '/data/chicago_taxi_trips_2020.parquet'
gdown.download(
    'https://drive.google.com/uc?id=1QLBGFOoKw_3-iM58q4unWfwHmPqfnrYr',
    file_path,
    quiet=False)

# Reading of parquet data
table2 = pq.read_table(file_path)

df = table2.to_pandas()
df.reset_index(inplace=True)

# Dividing data in chunks


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


mongo_uri = "mongodb://root:123456@0.0.0.0:27017/admin"
client = MongoClient(mongo_uri)
database = client.admin
collection = database['trips']
collection.remove()

# insertion of data in monngodb in sequence manner
for i in chunker(df, 50000):
    print('Total Inserted rows ', i.index[-1])
    collection.insert_many(i.to_dict(orient='records'))

# Indexing in db for fast reterival - Indexing done after ETL so as to do fast bulk writing first as insert take time after indexing
collection.create_index('trip_start_timestamp')
collection.create_index('trip_end_timestamp')
print(collection.index_information())
client.close()
