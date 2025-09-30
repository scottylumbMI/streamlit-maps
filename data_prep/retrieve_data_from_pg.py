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

#SQL to group by (dissolve) by as few fields as possible. intended to reduce record count
sql = '''
SELECT
    scale_site::text,
    species_code::text,
    product_code::text,
    region_harvested_description::text,
    mgmt_unit_type_description::text,
    mgmt_unit_id::text,
    EXTRACT(YEAR FROM scaling_date) AS year,
    EXTRACT(MONTH FROM scaling_date) AS month,
    SUM(total_volume_scaled) AS total_volume_scaled
FROM public.hbs_history
GROUP BY
    scale_site,
    species_code,
    product_code,
    region_harvested_description,
    mgmt_unit_type_description,
    mgmt_unit_id,
    year,
    month
'''


# read in chunks takes 20gb of ram if loaded at once
chunks = pd.read_sql(sql, engine, chunksize=50000)

for i, chunk in enumerate(chunks):
    
    print (f"running chunk {i} ")


    # append to parquet
    chunk.to_parquet(
        r"C:/Users/Scotty Lumb/code/python/streamlit-maps/data/hbs_history.parquet", 
        index=False, 
        engine="fastparquet",
        compression="gzip",
        append=True if i > 0 else False
    )
