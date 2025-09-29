import streamlit as st
import leafmap.foliumap as leafmap
import os
from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
import geopandas as gpd
import plotly.express as px



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

col_map, col_chart = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("OpenTopoMap")

gdf_regions = gdf_import()

with col_map:
    m = leafmap.Map(
        locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
    )
    
    m.add_gdf(gdf_regions, layer_name="Regions")
    basemap = st.selectbox("Select a basemap:", options, index)
    m.add_basemap(basemap)

    # Use selectbox for region selection
    selected_name = st.selectbox("Select a region", gdf_regions["rgn_name"].tolist())


    m.to_streamlit(height=700, return_selected=True)


with col_chart:
    if selected_name:

        df_selected = gdf_regions[gdf_regions["rgn_name"] == selected_name]

        # Melt wide year columns into long format
        df_melted = df_selected.melt(
            id_vars=["rgn_name"], 
            value_vars=[f"vol_{y}" for y in range(2010, 2026)],
            var_name="Year",
            value_name="Total Volume"
        )
        df_melted["Year"] = df_melted["Year"].str.replace("vol_", "").astype(int)

        # Plot bar chart
        fig = px.bar(
            df_melted, 
            x="Year", 
            y="Total Volume", 
            title=f"Harvest Volume for {selected_name}",
            labels={"Total Volume": "Harvest Volume"}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Click a region on the map to see its harvest volume by year.")
