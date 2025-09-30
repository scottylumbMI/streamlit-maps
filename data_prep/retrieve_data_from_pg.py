# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 16:56:04 2025

@author: Scotty Lumb
"""
import os
from sqlalchemy import text
import pandas as pd
from sqlalchemy import create_engine
# Database parameters
db_name = '00000_harvest_billing_system'
db_host = 'teak.meristem.lan'
db_user = os.environ["PG_USER"]
db_pass = os.environ["PG_PASS"]

print("Creating database engine...")
engine = create_engine(f'postgresql://{db_user}:{db_pass}@{db_host}/{db_name}')

sql = '''
SELECT DISTINCT 
    'scale_site',
    'species_code',
    'product_code',
    'region_harvested_description',
    'mgmt_unit_type_description',
    'mgmt_unit_id'
FROM public.hbs_history
'''


# df = pd.read_sql(sql, engine)
# df.to_parquet(r"C:/Users/Scotty Lumb/code/python/streamlit-maps/data/hbs_history.parquet", index=False)


# read in chunks
chunks = pd.read_sql(sql, engine, chunksize=50000)

for i, chunk in enumerate(chunks):
    
    # Ensure scaling_date is datetime
    chunk['scaling_date'] = pd.to_datetime(chunk['scaling_date'], errors='coerce')
    
    # Create year and month columns
    chunk['year'] = chunk['scaling_date'].dt.year
    chunk['month'] = chunk['scaling_date'].dt.month
    
    # append to parquet
    chunk.to_parquet(
        r"C:/Users/Scotty Lumb/code/python/streamlit-maps/data/hbs_history.parquet", 
        index=False, 
        engine="fastparquet",
        compression="gzip",
        append=True if i > 0 else False
    )
