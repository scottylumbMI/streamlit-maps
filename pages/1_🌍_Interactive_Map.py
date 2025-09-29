import streamlit as st
import leafmap.foliumap as leafmap
import os
from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
import geopandas as gpd



def gdf_import():
    # Database parameters
    db_name = '00000_harvest_billing_system'
    db_host = 'teak.meristem.lan'
    db_user = os.environ["PG_USER"]
    db_pass = os.environ["PG_PASS"]
    
    print("Creating database engine...")
    engine = create_engine(f'postgresql://{db_user}:{db_pass}@{db_host}/{db_name}')

    sql = '''
        SELECT 
            r.rgn_name,
            r.geom,
            SUM(CASE WHEN EXTRACT(YEAR FROM h.scaling_date) = 2010 THEN h.total_volume_scaled ELSE 0 END) AS vol_2010,
            SUM(CASE WHEN EXTRACT(YEAR FROM h.scaling_date) = 2011 THEN h.total_volume_scaled ELSE 0 END) AS vol_2011,
            SUM(CASE WHEN EXTRACT(YEAR FROM h.scaling_date) = 2012 THEN h.total_volume_scaled ELSE 0 END) AS vol_2012,
            SUM(CASE WHEN EXTRACT(YEAR FROM h.scaling_date) = 2013 THEN h.total_volume_scaled ELSE 0 END) AS vol_2013,
            SUM(CASE WHEN EXTRACT(YEAR FROM h.scaling_date) = 2014 THEN h.total_volume_scaled ELSE 0 END) AS vol_2014,
            SUM(CASE WHEN EXTRACT(YEAR FROM h.scaling_date) = 2015 THEN h.total_volume_scaled ELSE 0 END) AS vol_2015,
            SUM(CASE WHEN EXTRACT(YEAR FROM h.scaling_date) = 2016 THEN h.total_volume_scaled ELSE 0 END) AS vol_2016,
            SUM(CASE WHEN EXTRACT(YEAR FROM h.scaling_date) = 2017 THEN h.total_volume_scaled ELSE 0 END) AS vol_2017,
            SUM(CASE WHEN EXTRACT(YEAR FROM h.scaling_date) = 2018 THEN h.total_volume_scaled ELSE 0 END) AS vol_2018,
            SUM(CASE WHEN EXTRACT(YEAR FROM h.scaling_date) = 2019 THEN h.total_volume_scaled ELSE 0 END) AS vol_2019,
            SUM(CASE WHEN EXTRACT(YEAR FROM h.scaling_date) = 2020 THEN h.total_volume_scaled ELSE 0 END) AS vol_2020,
            SUM(CASE WHEN EXTRACT(YEAR FROM h.scaling_date) = 2021 THEN h.total_volume_scaled ELSE 0 END) AS vol_2021,
            SUM(CASE WHEN EXTRACT(YEAR FROM h.scaling_date) = 2022 THEN h.total_volume_scaled ELSE 0 END) AS vol_2022,
            SUM(CASE WHEN EXTRACT(YEAR FROM h.scaling_date) = 2023 THEN h.total_volume_scaled ELSE 0 END) AS vol_2023,
            SUM(CASE WHEN EXTRACT(YEAR FROM h.scaling_date) = 2024 THEN h.total_volume_scaled ELSE 0 END) AS vol_2024,
            SUM(CASE WHEN EXTRACT(YEAR FROM h.scaling_date) = 2025 THEN h.total_volume_scaled ELSE 0 END) AS vol_2025
        FROM app_display.nr_regions r
        LEFT JOIN public.hbs_history h
            ON r.rgn_name = h.region_harvested_description
        GROUP BY r.rgn_name, r.geom;
    '''
    # Load GeoDataFrame (assume geom column is 'geom')
    gdf = gpd.read_postgis(sql, engine, geom_col='geom')
    

    
    return gdf




markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)


st.title("Interactive Map")

col1, col2 = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("OpenTopoMap")

gdf_path_regions = r"C:\Users\Scotty Lumb\code\python\streamlit-maps\data\nr_regions.shp"

gdf_regions = gdf_import()

with col2:

    basemap = st.selectbox("Select a basemap:", options, index)


with col1:

    m = leafmap.Map(
        locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
    )
        
    m.add_gdf(gdf_regions, layer_name="Regions")
    # # Add shapefile if it exists
    # if os.path.exists(gdf_path_regions):
    #     m.add_shp(gdf_path_regions, layer_name="Resource Regions")
    # else:
    #     st.warning(f"Shapefile not found at {gdf_path_regions}")
        
    m.add_basemap(basemap)
    m.to_streamlit(height=700)
